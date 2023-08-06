"""
Manager and Serializers for Quotas.

For more information about quotas: https://galaxyproject.org/admin/disk-quotas/
"""
import logging
from typing import (
    cast,
    Optional,
    Tuple,
    Union,
)

from sqlalchemy import (
    false,
    true
)

from galaxy import model, util
from galaxy.app import StructuredApp
from galaxy.exceptions import ActionInputError
from galaxy.managers import base
from galaxy.managers.context import ProvidesUserContext
from galaxy.quota import DatabaseQuotaAgent
from galaxy.quota._schema import (
    CreateQuotaParams,
    CreateQuotaResult,
    DefaultQuotaValues,
    DeleteQuotaPayload,
    QuotaDetails,
    QuotaOperation,
    QuotaSummaryList,
    UpdateQuotaParams,
)
from galaxy.schema.fields import EncodedDatabaseIdField
from galaxy.web import url_for

log = logging.getLogger(__name__)


class QuotaManager:
    """Interface/service object to interact with Quotas."""

    def __init__(self, app: StructuredApp):
        self.app = app

    @property
    def sa_session(self):
        return self.app.model.context

    @property
    def quota_agent(self) -> DatabaseQuotaAgent:
        return cast(DatabaseQuotaAgent, self.app.quota_agent)

    def create_quota(self, payload: dict, decode_id=None) -> Tuple[model.Quota, str]:
        params = CreateQuotaParams.parse_obj(payload)
        create_amount = self._parse_amount(params.amount)
        if self.sa_session.query(model.Quota).filter(model.Quota.name == params.name).first():
            raise ActionInputError("Quota names must be unique and a quota with that name already exists, please choose another name.")
        elif create_amount is False:
            raise ActionInputError("Unable to parse the provided amount.")
        elif params.operation not in model.Quota.valid_operations:
            raise ActionInputError("Enter a valid operation.")
        elif params.default != DefaultQuotaValues.NO and params.operation != QuotaOperation.EXACT:
            raise ActionInputError("Operation for a default quota must be '='.")
        elif create_amount is None and params.operation != QuotaOperation.EXACT:
            raise ActionInputError("Operation for an unlimited quota must be '='.")
        # Create the quota
        quota = model.Quota(name=params.name, description=params.description, amount=create_amount, operation=params.operation)
        self.sa_session.add(quota)
        # If this is a default quota, create the DefaultQuotaAssociation
        if params.default != DefaultQuotaValues.NO:
            self.quota_agent.set_default_quota(params.default, quota)
            message = f"Default quota '{quota.name}' has been created."
        else:
            # Create the UserQuotaAssociations
            in_users = [self.sa_session.query(model.User).get(decode_id(x) if decode_id else x) for x in util.listify(params.in_users)]
            in_groups = [self.sa_session.query(model.Group).get(decode_id(x) if decode_id else x) for x in util.listify(params.in_groups)]
            if None in in_users:
                raise ActionInputError("One or more invalid user id has been provided.")
            for user in in_users:
                uqa = model.UserQuotaAssociation(user, quota)
                self.sa_session.add(uqa)
            # Create the GroupQuotaAssociations
            if None in in_groups:
                raise ActionInputError("One or more invalid group id has been provided.")
            for group in in_groups:
                gqa = model.GroupQuotaAssociation(group, quota)
                self.sa_session.add(gqa)
            message = f"Quota '{quota.name}' has been created with {len(in_users)} associated users and {len(in_groups)} associated groups."
        self.sa_session.flush()
        return quota, message

    def _parse_amount(self, amount: str) -> Optional[Union[int, bool]]:
        if amount.lower() in ('unlimited', 'none', 'no limit'):
            return None
        try:
            return util.size_to_bytes(amount)
        except AssertionError:
            return False

    def rename_quota(self, quota, params) -> str:
        if not params.name:
            raise ActionInputError('Enter a valid name.')
        elif params.name != quota.name and self.sa_session.query(model.Quota).filter(model.Quota.name == params.name).first():
            raise ActionInputError('A quota with that name already exists.')
        else:
            old_name = quota.name
            quota.name = params.name
            if params.description:
                quota.description = params.description
            self.sa_session.add(quota)
            self.sa_session.flush()
            message = f"Quota '{old_name}' has been renamed to '{params.name}'."
            return message

    def manage_users_and_groups_for_quota(self, quota, params, decode_id=None) -> str:
        if quota.default:
            raise ActionInputError('Default quotas cannot be associated with specific users and groups.')
        else:
            in_users = [self.sa_session.query(model.User).get(decode_id(x) if decode_id else x) for x in util.listify(params.in_users)]
            if None in in_users:
                raise ActionInputError("One or more invalid user id has been provided.")
            in_groups = [self.sa_session.query(model.Group).get(decode_id(x) if decode_id else x) for x in util.listify(params.in_groups)]
            if None in in_groups:
                raise ActionInputError("One or more invalid group id has been provided.")
            self.quota_agent.set_entity_quota_associations(quotas=[quota], users=in_users, groups=in_groups)
            self.sa_session.refresh(quota)
            message = f"Quota '{quota.name}' has been updated with {len(in_users)} associated users and {len(in_groups)} associated groups."
            return message

    def edit_quota(self, quota, params) -> str:
        if params.amount.lower() in ('unlimited', 'none', 'no limit'):
            new_amount = None
        else:
            try:
                new_amount = util.size_to_bytes(params.amount)
            except (AssertionError, ValueError):
                new_amount = False
        if not params.amount:
            raise ActionInputError('Enter a valid amount.')
        elif new_amount is False:
            raise ActionInputError('Unable to parse the provided amount.')
        elif params.operation not in model.Quota.valid_operations:
            raise ActionInputError('Enter a valid operation.')
        else:
            quota.amount = new_amount
            quota.operation = params.operation
            self.sa_session.add(quota)
            self.sa_session.flush()
            message = f"Quota '{quota.name}' is now '{quota.operation}{quota.display_amount}'."
            return message

    def set_quota_default(self, quota, params) -> str:
        if params.default != 'no' and params.default not in model.DefaultQuotaAssociation.types.__members__.values():
            raise ActionInputError('Enter a valid default type.')
        else:
            if params.default != 'no':
                self.quota_agent.set_default_quota(params.default, quota)
                message = f"Quota '{quota.name}' is now the default for {params.default} users."
            else:
                if quota.default:
                    message = f"Quota '{quota.name}' is no longer the default for {quota.default[0].type} users."
                    for dqa in quota.default:
                        self.sa_session.delete(dqa)
                    self.sa_session.flush()
                else:
                    message = f"Quota '{quota.name}' is not a default."
            return message

    def unset_quota_default(self, quota, params=None) -> str:
        if not quota.default:
            raise ActionInputError(f"Quota '{quota.name}' is not a default.")
        else:
            message = f"Quota '{quota.name}' is no longer the default for {quota.default[0].type} users."
            for dqa in quota.default:
                self.sa_session.delete(dqa)
            self.sa_session.flush()
            return message

    def delete_quota(self, quota, params=None) -> str:
        quotas = util.listify(quota)
        names = []
        for q in quotas:
            if q.default:
                names.append(q.name)
        if len(names) == 1:
            raise ActionInputError(f"Quota '{names[0]}' is a default, please unset it as a default before deleting it.")
        elif len(names) > 1:
            raise ActionInputError(f"Quotas are defaults, please unset them as defaults before deleting them: {', '.join(names)}")
        message = f"Deleted {len(quotas)} quotas: "
        for q in quotas:
            q.deleted = True
            self.sa_session.add(q)
            names.append(q.name)
        self.sa_session.flush()
        message += ', '.join(names)
        return message

    def undelete_quota(self, quota, params=None) -> str:
        quotas = util.listify(quota)
        names = []
        for q in quotas:
            if not q.deleted:
                names.append(q.name)
        if len(names) == 1:
            raise ActionInputError(f"Quota '{names[0]}' has not been deleted, so it cannot be undeleted.")
        elif len(names) > 1:
            raise ActionInputError(f"Quotas have not been deleted so they cannot be undeleted: {', '.join(names)}")
        message = f"Undeleted {len(quotas)} quotas: "
        for q in quotas:
            q.deleted = False
            self.sa_session.add(q)
            names.append(q.name)
        self.sa_session.flush()
        message += ', '.join(names)
        return message

    def purge_quota(self, quota, params=None):
        """
        This method should only be called for a Quota that has previously been deleted.
        Purging a deleted Quota deletes all of the following from the database:
        - UserQuotaAssociations where quota_id == Quota.id
        - GroupQuotaAssociations where quota_id == Quota.id
        """
        quotas = util.listify(quota)
        names = []
        for q in quotas:
            if not q.deleted:
                names.append(q.name)
        if len(names) == 1:
            raise ActionInputError(f"Quota '{names[0]}' has not been deleted, so it cannot be purged.")
        elif len(names) > 1:
            raise ActionInputError(f"Quotas have not been deleted so they cannot be undeleted: {', '.join(names)}")
        message = f"Purged {len(quotas)} quotas: "
        for q in quotas:
            # Delete UserQuotaAssociations
            for uqa in q.users:
                self.sa_session.delete(uqa)
            # Delete GroupQuotaAssociations
            for gqa in q.groups:
                self.sa_session.delete(gqa)
            names.append(q.name)
        self.sa_session.flush()
        message += ', '.join(names)
        return message

    def get_quota(self, trans, id: EncodedDatabaseIdField, deleted: Optional[bool] = None) -> model.Quota:
        return base.get_object(trans, id, 'Quota', check_ownership=False, check_accessible=False, deleted=deleted)


class QuotasService:
    """Interface/service object shared by controllers for interacting with quotas."""

    def __init__(self, app: StructuredApp):
        self.quota_manager: QuotaManager = QuotaManager(app)

    def index(self, trans: ProvidesUserContext, deleted: bool = False) -> QuotaSummaryList:
        """Displays a collection (list) of quotas."""
        rval = []
        query = trans.sa_session.query(model.Quota)
        if deleted:
            route = 'deleted_quota'
            query = query.filter(model.Quota.deleted == true())
        else:
            route = 'quota'
            query = query.filter(model.Quota.deleted == false())
        for quota in query:
            item = quota.to_dict(value_mapper={'id': trans.security.encode_id})
            encoded_id = trans.security.encode_id(quota.id)
            item['url'] = self._url_for(route, id=encoded_id)
            rval.append(item)
        return QuotaSummaryList.parse_obj(rval)

    def show(self, trans: ProvidesUserContext, id: EncodedDatabaseIdField, deleted: bool = False) -> QuotaDetails:
        """Displays information about a quota."""
        quota = self.quota_manager.get_quota(trans, id, deleted=deleted)
        rval = quota.to_dict(view='element', value_mapper={'id': trans.security.encode_id, 'total_disk_usage': float})
        return QuotaDetails.parse_obj(rval)

    def create(self, trans: ProvidesUserContext, params: CreateQuotaParams) -> CreateQuotaResult:
        """Creates a new quota."""
        payload = params.dict()
        self.validate_in_users_and_groups(trans, payload)
        quota, message = self.quota_manager.create_quota(payload)
        item = quota.to_dict(value_mapper={'id': trans.security.encode_id})
        item['url'] = self._url_for('quota', id=trans.security.encode_id(quota.id))
        item['message'] = message
        return CreateQuotaResult.parse_obj(item)

    def update(self, trans: ProvidesUserContext, id: EncodedDatabaseIdField, params: UpdateQuotaParams) -> str:
        """Modifies a quota."""
        payload = params.dict()
        self.validate_in_users_and_groups(trans, payload)
        quota = self.quota_manager.get_quota(trans, id, deleted=False)

        params = UpdateQuotaParams(**payload)
        # FIXME: Doing it this way makes the update non-atomic if a method fails after an earlier one has succeeded.
        methods = []
        if params.name or params.description:
            methods.append(self.quota_manager.rename_quota)
        if params.amount:
            methods.append(self.quota_manager.edit_quota)
        if params.default == DefaultQuotaValues.NO:
            methods.append(self.quota_manager.unset_quota_default)
        elif params.default:
            methods.append(self.quota_manager.set_quota_default)
        if params.in_users or params.in_groups:
            methods.append(self.quota_manager.manage_users_and_groups_for_quota)

        messages = []
        for method in methods:
            message = method(quota, params)
            messages.append(message)
        return '; '.join(messages)

    def delete(self, trans: ProvidesUserContext, id: EncodedDatabaseIdField, payload: Optional[DeleteQuotaPayload] = None) -> str:
        """Marks a quota as deleted."""
        quota = self.quota_manager.get_quota(trans, id, deleted=False)  # deleted quotas are not technically members of this collection
        message = self.quota_manager.delete_quota(quota)
        if payload and payload.purge:
            message += self.quota_manager.purge_quota(quota)
        return message

    def undelete(self, trans: ProvidesUserContext, id: EncodedDatabaseIdField) -> str:
        """Restores a previously deleted quota."""
        quota = self.quota_manager.get_quota(trans, id, deleted=True)
        return self.quota_manager.undelete_quota(quota)

    def validate_in_users_and_groups(self, trans, payload):
        """
        For convenience, in_users and in_groups can be encoded IDs or emails/group names in the API.
        """
        def get_id(item, model_class, column):
            try:
                return trans.security.decode_id(item)
            except Exception:
                pass  # maybe an email/group name
            # this will raise if the item is invalid
            return trans.sa_session.query(model_class).filter(column == item).first().id
        new_in_users = []
        new_in_groups = []
        invalid = []
        for item in util.listify(payload.get('in_users', [])):
            try:
                new_in_users.append(get_id(item, model.User, model.User.email))
            except Exception:
                invalid.append(item)
        for item in util.listify(payload.get('in_groups', [])):
            try:
                new_in_groups.append(get_id(item, model.Group, model.Group.name))
            except Exception:
                invalid.append(item)
        if invalid:
            msg = f"The following value(s) for associated users and/or groups could not be parsed: {', '.join(invalid)}."
            msg += "  Valid values are email addresses of users, names of groups, or IDs of both."
            raise Exception(msg)
        payload['in_users'] = list(map(str, new_in_users))
        payload['in_groups'] = list(map(str, new_in_groups))

    def _url_for(self, *args, **kargs):
        try:
            return url_for(*args, **kargs)
        except AttributeError:
            return "*deprecated attribute not filled in by FastAPI server*"
