from typing import Optional

from galaxy.managers.context import (
    ProvidesHistoryContext,
)
from galaxy.model import History


class WorkRequestContext(ProvidesHistoryContext):
    """ Stripped down implementation of Galaxy web transaction god object for
    work request handling outside of web threads - uses mix-ins shared with
    GalaxyWebTransaction to provide app, user, and history context convenience
    methods - but nothing related to HTTP handling, mako views, etc....

    Things that only need app shouldn't be consuming trans - but there is a
    need for actions potentially tied to users and histories and  hopefully
    this can define that stripped down interface providing access to user and
    history information - but not dealing with web request and response
    objects.
    """

    def __init__(self, app, user=None, history=None, workflow_building_mode=False, url_builder=None):
        self._app = app
        self.__user = user
        self.__user_current_roles = None
        self.__history = history
        self._url_builder = url_builder
        self.workflow_building_mode = workflow_building_mode

    @property
    def app(self):
        return self._app

    @property
    def url_builder(self):
        return self._url_builder

    def get_history(self, create=False):
        return self.__history

    @property
    def history(self):
        return self.get_history()

    def get_user(self):
        """Return the current user if logged in or None."""
        return self.__user

    def get_current_user_roles(self):
        if self.__user_current_roles is None:
            self.__user_current_roles = super().get_current_user_roles()
        return self.__user_current_roles

    def set_user(self, user):
        """Set the current user."""
        raise NotImplementedError("Cannot change users from a work request context.")

    user = property(get_user, set_user)


class SessionRequestContext(WorkRequestContext):
    """Like WorkRequestContext, but provides access to galaxy session and session."""

    def __init__(self, **kwargs):
        self.galaxy_session = kwargs.pop('galaxy_session', None)
        self._host = kwargs.pop("host")
        super().__init__(**kwargs)

    @property
    def host(self):
        return self._host

    def get_galaxy_session(self):
        return self.galaxy_session


def proxy_work_context_for_history(trans: ProvidesHistoryContext, history: Optional[History] = None, workflow_building_mode=False):
    """Create a WorkContext for supplied context with potentially different history.

    This provides semi-structured access to a transaction/work context with a supplied target
    history that is different from the user's current history (which also might change during
    the request).
    """
    return WorkRequestContext(app=trans.app, user=trans.user, history=history or trans.history, url_builder=trans.url_builder, workflow_building_mode=workflow_building_mode)
