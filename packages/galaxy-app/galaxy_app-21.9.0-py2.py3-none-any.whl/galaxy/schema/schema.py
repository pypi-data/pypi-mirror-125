"""This module contains general pydantic models and common schema field annotations for them."""

from datetime import datetime
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

from pydantic import (
    AnyHttpUrl,
    AnyUrl,
    BaseModel,
    Extra,
    Field,
    FilePath,
    Json,
    UUID4,
)

from galaxy.model import (
    Dataset,
    DatasetCollection,
    DatasetInstance,
    Job,
)
from galaxy.schema.fields import (
    EncodedDatabaseIdField,
    ModelClassField,
    optional,
)
from galaxy.schema.types import RelativeUrl

USER_MODEL_CLASS_NAME = "User"
GROUP_MODEL_CLASS_NAME = "Group"
HDA_MODEL_CLASS_NAME = "HistoryDatasetAssociation"
DC_MODEL_CLASS_NAME = "DatasetCollection"
DCE_MODEL_CLASS_NAME = "DatasetCollectionElement"
HDCA_MODEL_CLASS_NAME = "HistoryDatasetCollectionAssociation"
HISTORY_MODEL_CLASS_NAME = "History"
JOB_MODEL_CLASS_NAME = "Job"
STORED_WORKFLOW_MODEL_CLASS_NAME = "StoredWorkflow"


# Generic and common Field annotations that can be reused across models

RelativeUrlField: RelativeUrl = Field(
    ...,
    title="URL",
    description="The relative URL to access this item.",
    deprecated=True,
)

DownloadUrlField: RelativeUrl = Field(
    ...,
    title="Download URL",
    description="The URL to download this item from the server.",
)

AnnotationField: Optional[str] = Field(
    ...,
    title="Annotation",
    description="An annotation to provide details or to help understand the purpose and usage of this item.",
)

AccessibleField: bool = Field(
    ...,
    title="Accessible",
    description="Whether this item is accessible to the current user due to permissions.",
)

EncodedEntityIdField: EncodedDatabaseIdField = Field(
    ...,
    title="ID",
    description="The encoded ID of this entity.",
)

DatasetStateField: Dataset.states = Field(
    ...,
    title="State",
    description="The current state of this dataset.",
)

CreateTimeField: datetime = Field(
    ...,
    title="Create Time",
    description="The time and date this item was created.",
)

UpdateTimeField: datetime = Field(
    ...,
    title="Update Time",
    description="The last time and date this item was updated.",
)

CollectionTypeField: str = Field(
    ...,
    title="Collection Type",
    description=(
        "The type of the collection, can be `list`, `paired`, or define subcollections using `:` "
        "as separator like `list:paired` or `list:list`."
    ),
)

PopulatedStateField: DatasetCollection.populated_states = Field(
    ...,
    title="Populated State",
    description=(
        "Indicates the general state of the elements in the dataset collection:"
        "- 'new': new dataset collection, unpopulated elements."
        "- 'ok': collection elements populated (HDAs may or may not have errors)."
        "- 'failed': some problem populating, won't be populated."
    ),
)

PopulatedStateMessageField: Optional[str] = Field(
    None,
    title="Populated State Message",
    description="Optional message with further information in case the population of the dataset collection failed.",
)

ElementCountField: Optional[int] = Field(
    None,
    title="Element Count",
    description=(
        "The number of elements contained in the dataset collection. "
        "It may be None or undefined if the collection could not be populated."
    ),
)

PopulatedField: bool = Field(
    ...,
    title="Populated",
    description="Whether the dataset collection elements (and any subcollections elements) were successfully populated.",
)

ElementsField: List['DCESummary'] = Field(
    [],
    title="Elements",
    description="The summary information of each of the elements inside the dataset collection.",
)

HistoryIdField: EncodedDatabaseIdField = Field(
    ...,
    title="History ID",
    description="The encoded ID of the history associated with this item.",
)

UuidField: UUID4 = Field(
    ...,
    title="UUID",
    description="Universal unique identifier for this dataset.",
)

GenomeBuildField: Optional[str] = Field(
    "?",
    title="Genome Build",
    description="TODO",
)


class Model(BaseModel):
    """Base model definition with common configuration used by all derived models."""
    class Config:
        use_enum_values = True  # when using .dict()
        allow_population_by_field_name = True


class UserModel(Model):
    """User in a transaction context."""
    id: EncodedDatabaseIdField = Field(title='ID', description='User ID')
    username: str = Field(title='Username', description='User username')
    email: str = Field(title='Email', description='User email')
    active: bool = Field(title='Active', description='User is active')
    deleted: bool = Field(title='Deleted', description='User is deleted')
    last_password_change: datetime = Field(title='Last password change', description='')
    model_class: str = ModelClassField(USER_MODEL_CLASS_NAME)


class GroupModel(BaseModel):
    """User group model"""
    model_class: str = ModelClassField(GROUP_MODEL_CLASS_NAME)
    id: EncodedDatabaseIdField = Field(
        ...,  # Required
        title='ID',
        description='Encoded group ID',
    )
    name: str = Field(
        ...,  # Required
        title="Name",
        description="The name of the group.",
    )


class JobSourceType(str, Enum):
    """Available types of job sources (model classes) that produce dataset collections."""
    Job = "Job"
    ImplicitCollectionJobs = "ImplicitCollectionJobs"
    WorkflowInvocation = "WorkflowInvocation"


class HistoryContentType(str, Enum):
    """Available types of History contents."""
    dataset = "dataset"
    dataset_collection = "dataset_collection"


class HistoryImportArchiveSourceType(str, Enum):
    """Available types of History archive sources."""
    url = "url"
    file = "file"


class DCEType(str, Enum):  # TODO: suspiciously similar to HistoryContentType
    """Available types of dataset collection elements."""
    hda = "hda"
    dataset_collection = "dataset_collection"


class DatasetSourceType(str, Enum):
    hda = "hda"
    ldda = "ldda"


class ColletionSourceType(str, Enum):
    hda = "hda"
    ldda = "ldda"
    hdca = "hdca"
    new_collection = "new_collection"


class HistoryContentSource(str, Enum):
    hda = "hda"
    hdca = "hdca"
    library = "library"
    library_folder = "library_folder"
    new_collection = "new_collection"


class TagCollection(Model):
    """Represents the collection of tags associated with an item."""
    __root__: List[str] = Field(
        default=...,
        title="Tags",
        description="The collection of tags associated with an item.",
    )


class MetadataFile(Model):
    """Metadata file associated with a dataset."""
    file_type: str = Field(
        ...,
        title="File Type",
        description="TODO",
    )
    download_url: RelativeUrl = DownloadUrlField


class DatasetPermissions(Model):
    """Role-based permissions for accessing and managing a dataset."""
    manage: List[EncodedDatabaseIdField] = Field(
        [],
        title="Management",
        description="The set of roles (encoded IDs) that can manage this dataset.",
    )
    access: List[EncodedDatabaseIdField] = Field(
        [],
        title="Access",
        description="The set of roles (encoded IDs) that can access this dataset.",
    )


class Hyperlink(Model):
    """Represents some text with an Hyperlink."""
    target: str = Field(
        ...,
        title="Target",
        description="Specifies where to open the linked document.",
        example="_blank"
    )
    href: AnyUrl = Field(
        ...,
        title="HRef",
        description="Specifies the linked document, resource, or location.",
    )
    text: str = Field(
        ...,
        title="Text",
        description="The text placeholder for the link.",
    )


class DisplayApp(Model):
    """Basic linked information about an application that can display certain datatypes."""
    label: str = Field(
        ...,
        title="Label",
        description="The label or title of the Display Application.",
    )
    links: List[Hyperlink] = Field(
        ...,
        title="Links",
        description="The collection of link details for this Display Application.",
    )


class Visualization(Model):  # TODO annotate this model
    class Config:
        extra = Extra.allow  # Allow any fields temporarily until the model is annotated


class HistoryItemBase(Model):
    """Basic information provided by items contained in a History."""
    id: EncodedDatabaseIdField = EncodedEntityIdField
    name: str = Field(
        ...,
        title="Name",
        description="The name of the item.",
    )
    history_id: EncodedDatabaseIdField = HistoryIdField
    hid: int = Field(
        ...,
        title="HID",
        description="The index position of this item in the History.",
    )
    history_content_type: HistoryContentType = Field(
        ...,
        title="Content Type",
        description="The type of this item.",
    )
    deleted: bool = Field(
        ...,
        title="Deleted",
        description="Whether this item is marked as deleted.",
    )
    visible: bool = Field(
        ...,
        title="Visible",
        description="Whether this item is visible or hidden to the user by default.",
    )


class HistoryItemCommon(HistoryItemBase):
    """Common information provided by items contained in a History."""
    type_id: str = Field(
        ...,
        title="Type - ID",
        description="The type and the encoded ID of this item. Used for caching.",
        example="dataset-616e371b2cc6c62e",
    )
    type: str = Field(
        ...,
        title="Type",
        description="The type of this item.",
    )
    create_time: datetime = CreateTimeField
    update_time: datetime = UpdateTimeField
    url: RelativeUrl = RelativeUrlField
    tags: TagCollection


class HDASummary(HistoryItemCommon):
    """History Dataset Association summary information."""
    dataset_id: EncodedDatabaseIdField = Field(
        ...,
        title="Dataset ID",
        description="The encoded ID of the dataset associated with this item.",
    )
    state: Dataset.states = DatasetStateField
    extension: str = Field(
        ...,
        title="Extension",
        description="The extension of the dataset.",
        example="txt",
    )
    purged: bool = Field(
        ...,
        title="Purged",
        description="Whether this dataset has been removed from disk.",
    )


class HDAInaccessible(HistoryItemBase):
    """History Dataset Association information when the user can not access it."""
    accessible: bool = AccessibleField
    state: Dataset.states = DatasetStateField


class HDADetailed(HDASummary):
    """History Dataset Association detailed information."""
    model_class: str = ModelClassField(HDA_MODEL_CLASS_NAME)
    hda_ldda: DatasetSourceType = Field(
        DatasetSourceType.hda,
        const=True,
        title="HDA or LDDA",
        description="Whether this dataset belongs to a history (HDA) or a library (LDDA).",
        deprecated=False  # TODO Should this field be deprecated in favor of model_class?
    )
    accessible: bool = AccessibleField
    genome_build: Optional[str] = GenomeBuildField
    misc_info: str = Field(
        ...,
        title="Miscellaneous Information",
        description="TODO",
    )
    misc_blurb: str = Field(
        ...,
        title="Miscellaneous Blurb",
        description="TODO",
    )
    file_ext: str = Field(  # Is this a duplicate of HDASummary.extension?
        ...,
        title="File extension",
        description="The extension of the file.",
    )
    file_size: int = Field(
        ...,
        title="File Size",
        description="The file size in bytes.",
    )
    resubmitted: bool = Field(
        ...,
        title="Resubmitted",
        description="Whether the job creating this dataset has been resubmitted.",
    )
    metadata: Any = Field(  # TODO: create pydantic model for metadata?
        ...,
        title="Metadata",
        description="The metadata associated with this dataset.",
    )
    meta_files: List[MetadataFile] = Field(
        [],
        title="Metadata Files",
        description="Collection of metadata files associated with this dataset.",
    )
    data_type: str = Field(
        ...,
        title="Data Type",
        description="The fully qualified name of the class implementing the data type of this dataset.",
        example="galaxy.datatypes.data.Text"
    )
    peek: str = Field(
        ...,
        title="Peek",
        description="A few lines of contents from the start of the file.",
    )
    creating_job: str = Field(
        ...,
        title="Creating Job ID",
        description="The encoded ID of the job that created this dataset.",
    )
    rerunnable: bool = Field(
        ...,
        title="Rerunnable",
        description="Whether the job creating this dataset can be run again.",
    )
    uuid: UUID4 = UuidField
    permissions: DatasetPermissions = Field(
        ...,
        title="Permissions",
        description="Role-based access and manage control permissions for the dataset.",
    )
    file_name: FilePath = Field(
        ...,
        title="File Name",
        description="The full path to the dataset file.",
    )
    display_apps: List[DisplayApp] = Field(
        [],
        title="Display Applications",
        description="Contains new-style display app urls.",
    )
    display_types: List[DisplayApp] = Field(
        [],
        title="Legacy Display Applications",
        description="Contains old-style display app urls.",
        deprecated=False,  # TODO: Should this field be deprecated in favor of display_apps?
    )
    visualizations: List[Visualization] = Field(
        [],
        title="Visualizations",
        description="The collection of visualizations that can be applied to this dataset.",
    )
    validated_state: DatasetInstance.validated_states = Field(
        ...,
        title="Validated State",
        description="The state of the datatype validation for this dataset.",
    )
    validated_state_message: Optional[str] = Field(
        ...,
        title="Validated State Message",
        description="The message with details about the datatype validation result for this dataset.",
    )
    annotation: Optional[str] = AnnotationField
    download_url: RelativeUrl = DownloadUrlField
    type: str = Field(
        "file",
        const=True,
        title="Type",
        description="This is always `file` for datasets.",
    )
    api_type: str = Field(
        "file",
        const=True,
        title="API Type",
        description="TODO",
        deprecated=False,  # TODO: Should this field be deprecated as announced in release 16.04?
    )
    created_from_basename: Optional[str] = Field(
        None,
        title="Created from basename",
        description="The basename of the output that produced this dataset.",  # TODO: is that correct?
    )


class HDAExtended(HDADetailed):
    """History Dataset Association extended information."""
    tool_version: str = Field(
        ...,
        title="Tool Version",
        description="The version of the tool that produced this dataset.",
    )
    parent_id: Optional[EncodedDatabaseIdField] = Field(
        None,
        title="Parent ID",
        description="TODO",
    )
    designation: Optional[str] = Field(
        None,
        title="Designation",
        description="TODO",
    )


class HDABeta(HDADetailed):  # TODO: change HDABeta name to a more appropriate one.
    """History Dataset Association information used in the new Beta History."""
    # Equivalent to `betawebclient` serialization view for HDAs
    pass


@optional
class UpdateHDAPayload(HDABeta):
    """Used for updating a particular HDA. All fields are optional."""
    pass


class DCSummary(Model):
    """Dataset Collection summary information."""
    model_class: str = ModelClassField(DC_MODEL_CLASS_NAME)
    id: EncodedDatabaseIdField = EncodedEntityIdField
    create_time: datetime = CreateTimeField
    update_time: datetime = UpdateTimeField
    collection_type: str = CollectionTypeField
    populated_state: DatasetCollection.populated_states = PopulatedStateField
    populated_state_message: Optional[str] = PopulatedStateMessageField
    element_count: Optional[int] = ElementCountField


class DCESummary(Model):
    """Dataset Collection Element summary information."""
    id: EncodedDatabaseIdField = EncodedEntityIdField
    model_class: str = ModelClassField(DCE_MODEL_CLASS_NAME)
    element_index: int = Field(
        ...,
        title="Element Index",
        description="The position index of this element inside the collection.",
    )
    element_identifier: str = Field(
        ...,
        title="Element Identifier",
        description="The actual name of this element.",
    )
    element_type: DCEType = Field(
        ...,
        title="Element Type",
        description="The type of the element. Used to interpret the `object` field.",
    )
    object: Union[HDASummary, DCSummary] = Field(
        ...,
        title="Object",
        description="The element's specific data depending on the value of `element_type`.",
    )


class DCDetailed(DCSummary):
    """Dataset Collection detailed information."""
    populated: bool = PopulatedField
    elements: List[DCESummary] = ElementsField


class HDCASummary(HistoryItemCommon):
    """History Dataset Collection Association summary information."""
    model_class: str = ModelClassField(HDCA_MODEL_CLASS_NAME)  # TODO: inconsistency? HDASummary does not have model_class only the detailed view has it...
    type: str = Field(
        "collection",
        const=True,
        title="Type",
        description="This is always `collection` for dataset collections.",
    )
    collection_type: str = CollectionTypeField
    populated_state: DatasetCollection.populated_states = PopulatedStateField
    populated_state_message: Optional[str] = PopulatedStateMessageField
    element_count: Optional[int] = ElementCountField
    job_source_id: Optional[EncodedDatabaseIdField] = Field(
        None,
        title="Job Source ID",
        description="The encoded ID of the Job that produced this dataset collection. Used to track the state of the job.",
    )
    job_source_type: Optional[JobSourceType] = Field(
        None,
        title="Job Source Type",
        description="The type of job (model class) that produced this dataset collection. Used to track the state of the job.",
    )
    contents_url: RelativeUrl = Field(
        ...,
        title="Contents URL",
        description="The relative URL to access the contents of this dataset collection.",
    )


class HDCADetailed(HDCASummary):
    """History Dataset Collection Association detailed information."""
    populated: bool = PopulatedField
    elements: List[DCESummary] = ElementsField


@optional
class UpdateHDCAPayload(HDCADetailed):
    """Used for updating a particular HDCA. All fields are optional."""
    pass


class UpdateHistoryContentsBatchPayload(BaseModel):
    class Config:
        use_enum_values = True  # when using .dict()
        allow_population_by_field_name = True
        extra = Extra.allow  # Allow any additional field

    items: List[Union[UpdateHDAPayload, UpdateHDCAPayload]] = Field(
        ...,
        title="Items",
        description="A list of content items to update with the changes.",
    )
    deleted: Optional[bool] = Field(
        default=False,
        title="Deleted",
        description=(
            "This will check the uploading state if not deleting (i.e: deleted=False), "
            "otherwise cannot delete uploading files, so it will raise an error."
        ),
    )
    visible: Optional[bool] = Field(
        default=False,
        title="Visible",
        description=(
            "Show or hide history contents"
        ),
    )


class HistoryBase(BaseModel):
    """Provides basic configuration for all the History models."""
    class Config:
        use_enum_values = True  # When using .dict()
        extra = Extra.allow  # Allow any other extra fields


class HistorySummary(HistoryBase):
    """History summary information."""
    model_class: str = ModelClassField(HISTORY_MODEL_CLASS_NAME)
    id: EncodedDatabaseIdField = EncodedEntityIdField
    name: str = Field(
        ...,
        title="Name",
        description="The name of the history.",
    )
    deleted: bool = Field(
        ...,
        title="Deleted",
        description="Whether this item is marked as deleted.",
    )
    purged: bool = Field(
        ...,
        title="Purged",
        description="Whether this item has been permanently removed.",
    )
    url: RelativeUrl = RelativeUrlField
    published: bool = Field(
        ...,
        title="Published",
        description="Whether this resource is currently publicly available to all users.",
    )
    annotation: Optional[str] = AnnotationField
    tags: TagCollection


class HistoryActiveContentCounts(Model):
    """Contains the number of active, deleted or hidden items in a History."""
    active: int = Field(
        ...,
        title="Active",
        description="Number of active datasets.",
    )
    hidden: int = Field(
        ...,
        title="Hidden",
        description="Number of hidden datasets.",
    )
    deleted: int = Field(
        ...,
        title="Deleted",
        description="Number of deleted datasets.",
    )


HistoryStateCounts = Dict[Dataset.states, int]
HistoryStateIds = Dict[Dataset.states, List[EncodedDatabaseIdField]]


class HistoryDetailed(HistorySummary):  # Equivalent to 'dev-detailed' view, which seems the default
    """History detailed information."""
    contents_url: RelativeUrl = Field(
        ...,
        title="Contents URL",
        description="The relative URL to access the contents of this History.",
    )
    size: int = Field(
        ...,
        title="Size",
        description="The total size of the contents of this history in bytes.",
    )
    user_id: EncodedDatabaseIdField = Field(
        ...,
        title="User ID",
        description="The encoded ID of the user that owns this History.",
    )
    create_time: datetime = CreateTimeField
    update_time: datetime = UpdateTimeField
    importable: bool = Field(
        ...,
        title="Importable",
        description="Whether this History can be imported by other users with a shared link.",
    )
    slug: Optional[str] = Field(
        None,
        title="Slug",
        description="Part of the URL to uniquely identify this History by link in a readable way.",
    )
    username_and_slug: Optional[str] = Field(
        None,
        title="Username and slug",
        description="The relative URL in the form of /u/{username}/h/{slug}",
    )
    genome_build: Optional[str] = GenomeBuildField
    state: Dataset.states = Field(
        ...,
        title="State",
        description="The current state of the History based on the states of the datasets it contains.",
    )
    state_ids: HistoryStateIds = Field(
        ...,
        title="State IDs",
        description=(
            "A dictionary keyed to possible dataset states and valued with lists "
            "containing the ids of each HDA in that state."
        ),
    )
    state_details: HistoryStateCounts = Field(
        ...,
        title="State Counts",
        description=(
            "A dictionary keyed to possible dataset states and valued with the number "
            "of datasets in this history that have those states."
        ),
    )


class HistoryBeta(HistoryDetailed):
    """History detailed information used in the new Beta History."""
    annotation: Optional[str] = AnnotationField
    empty: bool = Field(
        ...,
        title="Empty",
        description="Whether this History has any content.",
    )
    nice_size: str = Field(
        ...,
        title="Nice Size",
        description="Human-readable size of the contents of this history.",
        example="95.4 MB"
    )
    purged: bool = Field(
        ...,
        title="Purged",
        description="Whether this History has been permanently removed.",
    )
    tags: TagCollection
    hid_counter: int = Field(
        ...,
        title="HID Counter",
        description="TODO",
    )
    contents_active: HistoryActiveContentCounts = Field(
        ...,
        title="Active Contents",
        description="Contains the number of active, deleted or hidden items in the History.",
    )


class ExportHistoryArchivePayload(Model):
    gzip: Optional[bool] = Field(
        default=True,
        title="GZip",
        description="Whether to export as gzip archive.",
    )
    include_hidden: Optional[bool] = Field(
        default=False,
        title="Include Hidden",
        description="Whether to include hidden datasets in the exported archive.",
    )
    include_deleted: Optional[bool] = Field(
        default=False,
        title="Include Deleted",
        description="Whether to include deleted datasets in the exported archive.",
    )
    file_name: Optional[str] = Field(
        default=None,
        title="File Name",
        description="The name of the file containing the exported history.",
    )
    directory_uri: Optional[str] = Field(
        default=None,
        title="Directory URI",
        description=(
            "A writable directory destination where the history will be exported "
            "using the `galaxy.files` URI infrastructure."
        ),
    )
    force: Optional[bool] = Field(  # Hack to force rebuild everytime during dev
        default=None,
        title="Force Rebuild",
        description="Whether to force a rebuild of the history archive.",
        hidden=True,  # Avoids displaying this field in the documentation
    )


class CreateHistoryPayload(Model):
    name: Optional[str] = Field(
        default=None,
        title="Name",
        description="The new history name.",
    )
    history_id: Optional[EncodedDatabaseIdField] = Field(
        default=None,
        title="History ID",
        description=(
            "The encoded ID of the history to copy. "
            "Provide this value only if you want to copy an existing history."
        ),
    )
    all_datasets: Optional[bool] = Field(
        default=True,
        title="All Datasets",
        description=(
            "Whether to copy also deleted HDAs/HDCAs. Only applies when "
            "providing a `history_id` to copy from."
        ),
    )
    archive_source: Optional[str] = Field(
        default=None,
        title="Archive Source",
        description=(
            "The URL that will generate the archive to import when `archive_type='url'`. "
            # This seems a bit odd but the create history action expects `archive_source` to be != None
            "When importing from a file using `archive_file`, please set `archive_source=''`."
        ),
    )
    archive_type: Optional[HistoryImportArchiveSourceType] = Field(
        default=HistoryImportArchiveSourceType.url,
        title="Archive Type",
        description="The type of source from where the new history will be imported.",
    )
    archive_file: Optional[Any] = Field(
        default=None,
        title="Archive File",
        description="Detailed file information when importing the history from a file.",
    )


class JobExportHistoryArchive(Model):
    id: EncodedDatabaseIdField = Field(
        ...,
        title="ID",
        description="The encoded database ID of the job that is currently processing a particular request.",
    )
    job_id: EncodedDatabaseIdField = Field(
        ...,
        title="Job ID",
        description="The encoded database ID of the job that generated this history export archive.",
    )
    ready: bool = Field(
        ...,
        title="Ready",
        description="Whether the export history job has completed successfully and the archive is ready to download",
    )
    preparing: bool = Field(
        ...,
        title="Preparing",
        description="Whether the history archive is currently being built or in preparation.",
    )
    up_to_date: bool = Field(
        ...,
        title="Up to Date",
        description="False, if a new export archive should be generated for the corresponding history.",
    )
    download_url: RelativeUrl = Field(
        ...,
        title="Download URL",
        description="Relative API URL to download the exported history archive.",
    )
    external_download_latest_url: AnyUrl = Field(
        ...,
        title="External Download Latest URL",
        description="Fully qualified URL to download the latests version of the exported history archive.",
    )
    external_download_permanent_url: AnyUrl = Field(
        ...,
        title="External Download Permanent URL",
        description="Fully qualified URL to download this particular version of the exported history archive.",
    )


class LabelValuePair(BaseModel):
    """Generic Label/Value pair model."""
    label: str = Field(
        ...,
        title="Label",
        description="The label of the item.",
    )
    value: str = Field(
        ...,
        title="Value",
        description="The value of the item.",
    )


class CustomBuildsMetadataResponse(BaseModel):
    installed_builds: List[LabelValuePair] = Field(
        ...,
        title="Installed Builds",
        description="TODO",
    )
    fasta_hdas: List[LabelValuePair] = Field(
        ...,
        title="Fasta HDAs",
        description=(
            "A list of label/value pairs with all the datasets of type `FASTA` contained in the History.\n"
            " - `label` is item position followed by the name of the dataset.\n"
            " - `value` is the encoded database ID of the dataset.\n"
        ),
    )


class JobIdResponse(BaseModel):
    """Contains the ID of the job associated with a particular request."""
    job_id: EncodedDatabaseIdField = Field(
        ...,
        title="Job ID",
        description="The encoded database ID of the job that is currently processing a particular request.",
    )


class HDCJobStateSummary(Model):
    """Overview of the job states working inside a dataset collection."""
    all_jobs: int = Field(
        0,
        title="All jobs",
        description="Total number of jobs associated with a dataset collection.",
    )
    new: int = Field(
        0,
        title="New jobs",
        description="Number of jobs in the `new` state.",
    )
    waiting: int = Field(
        0,
        title="Waiting jobs",
        description="Number of jobs in the `waiting` state.",
    )
    running: int = Field(
        0,
        title="Running jobs",
        description="Number of jobs in the `running` state.",
    )
    error: int = Field(
        0,
        title="Jobs with errors",
        description="Number of jobs in the `error` state.",
    )
    paused: int = Field(
        0,
        title="Paused jobs",
        description="Number of jobs in the `paused` state.",
    )
    deleted_new: int = Field(
        0,
        title="Deleted new jobs",
        description="Number of jobs in the `deleted_new` state.",
    )
    resubmitted: int = Field(
        0,
        title="Resubmitted jobs",
        description="Number of jobs in the `resubmitted` state.",
    )
    queued: int = Field(
        0,
        title="Queued jobs",
        description="Number of jobs in the `queued` state.",
    )
    ok: int = Field(
        0,
        title="OK jobs",
        description="Number of jobs in the `ok` state.",
    )
    failed: int = Field(
        0,
        title="Failed jobs",
        description="Number of jobs in the `failed` state.",
    )
    deleted: int = Field(
        0,
        title="Deleted jobs",
        description="Number of jobs in the `deleted` state.",
    )
    upload: int = Field(
        0,
        title="Upload jobs",
        description="Number of jobs in the `upload` state.",
    )


class HDCABeta(HDCADetailed):  # TODO: change HDCABeta name to a more appropriate one.
    """History Dataset Collection Association information used in the new Beta History."""
    # Equivalent to `betawebclient` serialization view for HDCAs
    collection_id: EncodedDatabaseIdField = Field(
        # TODO: inconsistency? the equivalent counterpart for HDAs, `dataset_id`, is declared in `HDASummary` scope
        # while in HDCAs it is only serialized in the new `betawebclient` view?
        ...,
        title="Collection ID",
        description="The encoded ID of the dataset collection associated with this HDCA.",
    )
    job_state_summary: Optional[HDCJobStateSummary] = Field(
        None,
        title="Job State Summary",
        description="Overview of the job states working inside the dataset collection.",
    )


class JobBaseModel(Model):
    id: EncodedDatabaseIdField = EncodedEntityIdField
    model_class: str = ModelClassField(JOB_MODEL_CLASS_NAME)
    tool_id: str = Field(
        ...,
        title="Tool ID",
        description="Identifier of the tool that generated this job.",
    )
    history_id: Optional[EncodedDatabaseIdField] = Field(
        None,
        title="History ID",
        description="The encoded ID of the history associated with this item.",
    )
    state: Job.states = Field(
        ...,
        title="State",
        description="Current state of the job.",
    )
    exit_code: Optional[int] = Field(
        None,
        title="Exit Code",
        description="The exit code returned by the tool. Can be unset if the job is not completed yet.",
    )
    create_time: datetime = CreateTimeField
    update_time: datetime = UpdateTimeField
    galaxy_version: str = Field(
        ...,
        title="Galaxy Version",
        description="The (major) version of Galaxy used to create this job.",
        example="21.05"
    )


class JobImportHistoryResponse(JobBaseModel):
    message: str = Field(
        ...,
        title="Message",
        description="Text message containing information about the history import.",
    )


class JobStateSummary(Model):
    id: EncodedDatabaseIdField = EncodedEntityIdField
    model: str = ModelClassField("Job")
    populated_state: DatasetCollection.populated_states = PopulatedStateField
    states: Dict[Job.states, int] = Field(
        {},
        title="States",
        description=(
            "A dictionary of job states and the number of jobs in that state."
        )
    )


class ImplicitCollectionJobsStateSummary(JobStateSummary):
    model: str = ModelClassField("ImplicitCollectionJobs")


class WorkflowInvocationStateSummary(JobStateSummary):
    model: str = ModelClassField("WorkflowInvocation")


class JobSummary(JobBaseModel):
    """Basic information about a job."""
    external_id: Optional[str] = Field(
        None,
        title="External ID",
        description=(
            "The job id used by the external job runner (Condor, Pulsar, etc.)"
            "Only administrator can see this value."
        )
    )
    command_line: Optional[str] = Field(
        None,
        title="Command Line",
        description=(
            "The command line produced by the job. "
            "Users can see this value if allowed in the configuration, administrator can always see this value."
        ),
    )
    user_email: Optional[str] = Field(
        None,
        title="User Email",
        description=(
            "The email of the user that owns this job. "
            "Only the owner of the job and administrators can see this value."
        ),
    )


class DatasetJobInfo(Model):
    id: EncodedDatabaseIdField = EncodedEntityIdField
    src: DatasetSourceType = Field(
        ...,
        title="Source",
        description="The source of this dataset, either `hda` or `ldda` depending of its origin.",
    )
    uuid: UUID4 = UuidField


class JobDetails(JobSummary):
    command_version: str = Field(
        ...,
        title="Command Version",
        description="Tool version indicated during job execution.",
    )
    params: Any = Field(
        ...,
        title="Parameters",
        description=(
            "Object containing all the parameters of the tool associated with this job. "
            "The specific parameters depend on the tool itself."
        ),
    )
    inputs: Dict[str, DatasetJobInfo] = Field(
        {},
        title="Inputs",
        description="Dictionary mapping all the tool inputs (by name) with the corresponding dataset information.",
    )
    outputs: Dict[str, DatasetJobInfo] = Field(
        {},
        title="Outputs",
        description="Dictionary mapping all the tool outputs (by name) with the corresponding dataset information.",
    )


class JobMetric(Model):
    title: str = Field(
        ...,
        title="Title",
        description="A descriptive title for this metric.",
    )
    value: str = Field(
        ...,
        title="Value",
        description="The textual representation of the metric value.",
    )
    plugin: str = Field(
        ...,
        title="Plugin",
        description="The instrumenter plugin that generated this metric.",
    )
    name: str = Field(
        ...,
        title="Name",
        description="The name of the metric variable.",
    )
    raw_value: str = Field(
        ...,
        title="Raw Value",
        description="The raw value of the metric as a string.",
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "Job Start Time",
                "value": "2021-02-25 14:55:40",
                "plugin": "core",
                "name": "start_epoch",
                "raw_value": "1614261340.0000000"
            }
        }


class JobMetricCollection(Model):
    """Represents a collection of metrics associated with a Job."""
    __root__: List[JobMetric] = Field(
        [],
        title="Job Metrics",
        description="Collections of metrics provided by `JobInstrumenter` plugins on a particular job.",
    )


class JobFullDetails(JobDetails):
    tool_stdout: str = Field(
        ...,
        title="Tool Standard Output",
        description="The captured standard output of the tool executed by the job.",
    )
    tool_stderr: str = Field(
        ...,
        title="Tool Standard Error",
        description="The captured standard error of the tool executed by the job.",
    )
    job_stdout: str = Field(
        ...,
        title="Job Standard Output",
        description="The captured standard output of the job execution.",
    )
    job_stderr: str = Field(
        ...,
        title="Job Standard Error",
        description="The captured standard error of the job execution.",
    )
    stdout: str = Field(  # Redundant? it seems to be (tool_stdout + "\n" + job_stdout)
        ...,
        title="Standard Output",
        description="Combined tool and job standard output streams.",
    )
    stderr: str = Field(  # Redundant? it seems to be (tool_stderr + "\n" + job_stderr)
        ...,
        title="Standard Error",
        description="Combined tool and job standard error streams.",
    )
    job_messages: List[str] = Field(
        ...,
        title="Job Messages",
        description="List with additional information and possible reasons for a failed job.",
    )
    job_metrics: Optional[JobMetricCollection] = Field(
        None,
        title="Job Metrics",
        description=(
            "Collections of metrics provided by `JobInstrumenter` plugins on a particular job. "
            "Only administrators can see these metrics."
        ),
    )


class StoredWorkflowSummary(Model):
    id: EncodedDatabaseIdField = EncodedEntityIdField
    model_class: str = ModelClassField(STORED_WORKFLOW_MODEL_CLASS_NAME)
    create_time: datetime = CreateTimeField
    update_time: datetime = UpdateTimeField
    name: str = Field(
        ...,
        title="Name",
        description="The name of the history.",
    )
    url: RelativeUrl = RelativeUrlField
    published: bool = Field(
        ...,
        title="Published",
        description="Whether this workflow is currently publicly available to all users.",
    )
    annotations: List[str] = Field(  # Inconsistency? Why workflows summaries use a list instead of an optional string?
        ...,
        title="Annotations",
        description="An list of annotations to provide details or to help understand the purpose and usage of this workflow.",
    )
    tags: TagCollection
    deleted: bool = Field(
        ...,
        title="Deleted",
        description="Whether this item is marked as deleted.",
    )
    hidden: bool = Field(
        ...,
        title="Hidden",
        description="TODO",
    )
    owner: str = Field(
        ...,
        title="Owner",
        description="The name of the user who owns this workflow.",
    )
    latest_workflow_uuid: UUID4 = Field(  # Is this really used?
        ...,
        title="Latest workflow UUID",
        description="TODO",
    )
    number_of_steps: int = Field(
        ...,
        title="Number of Steps",
        description="The number of steps that make up this workflow.",
    )
    show_in_tool_panel: bool = Field(
        ...,
        title="Show in Tool Panel",
        description="Whether to display this workflow in the Tools Panel.",
    )


class WorkflowInput(BaseModel):
    label: str = Field(
        ...,
        title="Label",
        description="Label of the input.",
    )
    value: str = Field(
        ...,
        title="Value",
        description="TODO",
    )
    uuid: UUID4 = Field(
        ...,
        title="UUID",
        description="Universal unique identifier of the input.",
    )


class WorkflowOutput(BaseModel):
    label: Optional[str] = Field(
        None,
        title="Label",
        description="Label of the output.",
    )
    output_name: str = Field(
        ...,
        title="Output Name",
        description="The name assigned to the output.",
    )
    uuid: Optional[UUID4] = Field(
        ...,
        title="UUID",
        description="Universal unique identifier of the output.",
    )


class InputStep(BaseModel):
    source_step: int = Field(
        ...,
        title="Source Step",
        description="The identifier of the workflow step connected to this particular input.",
    )
    step_output: str = Field(
        ...,
        title="Step Output",
        description="The name of the output generated by the source step.",
    )


class WorkflowModuleType(str, Enum):
    """Available types of modules that represent a step in a Workflow."""
    data_input = "data_input"
    data_collection_input = "data_collection_input"
    parameter_input = "parameter_input"
    subworkflow = "subworkflow"
    tool = "tool"
    pause = "pause"  # Experimental


class WorkflowStepBase(BaseModel):
    id: int = Field(
        ...,
        title="ID",
        description="The identifier of the step. It matches the index order of the step inside the workflow."
    )
    type: WorkflowModuleType = Field(
        ...,
        title="Type",
        description="The type of workflow module."
    )
    annotation: Optional[str] = AnnotationField
    input_steps: Dict[str, InputStep] = Field(
        ...,
        title="Input Steps",
        description="A dictionary containing information about the inputs connected to this workflow step."
    )


class ToolBasedWorkflowStep(WorkflowStepBase):
    tool_id: Optional[str] = Field(
        None,
        title="Tool ID",
        description="The unique name of the tool associated with this step."
    )
    tool_version: Optional[str] = Field(
        None,
        title="Tool Version",
        description="The version of the tool associated with this step."
    )
    tool_inputs: Any = Field(
        ...,
        title="Tool Inputs",
        description="TODO"
    )


class InputDataStep(ToolBasedWorkflowStep):
    type: WorkflowModuleType = Field(
        WorkflowModuleType.data_input, const=True,
        title="Type",
        description="The type of workflow module."
    )


class InputDataCollectionStep(ToolBasedWorkflowStep):
    type: WorkflowModuleType = Field(
        WorkflowModuleType.data_collection_input, const=True,
        title="Type",
        description="The type of workflow module."
    )


class InputParameterStep(ToolBasedWorkflowStep):
    type: WorkflowModuleType = Field(
        WorkflowModuleType.parameter_input, const=True,
        title="Type",
        description="The type of workflow module."
    )


class PauseStep(WorkflowStepBase):
    type: WorkflowModuleType = Field(
        WorkflowModuleType.pause, const=True,
        title="Type",
        description="The type of workflow module."
    )


class ToolStep(ToolBasedWorkflowStep):
    type: WorkflowModuleType = Field(
        WorkflowModuleType.tool, const=True,
        title="Type",
        description="The type of workflow module."
    )


class SubworkflowStep(WorkflowStepBase):
    type: WorkflowModuleType = Field(
        WorkflowModuleType.subworkflow, const=True,
        title="Type",
        description="The type of workflow module."
    )
    workflow_id: EncodedDatabaseIdField = Field(
        ...,
        title="Workflow ID",
        description="The encoded ID of the workflow that will be run on this step."
    )


class Creator(BaseModel):
    class_: str = Field(
        ...,
        alias="class",
        title="Class",
        description="The class representing this creator."
    )
    name: str = Field(
        ...,
        title="Name",
        description="The name of the creator."
    )
    address: Optional[str] = Field(
        None,
        title="Address",
    )
    alternate_name: Optional[str] = Field(
        None,
        alias="alternateName",
        title="Alternate Name",
    )
    email: Optional[str] = Field(
        None,
        title="Email",
    )
    fax_number: Optional[str] = Field(
        None,
        alias="faxNumber",
        title="Fax Number",
    )
    identifier: Optional[str] = Field(
        None,
        title="Identifier",
        description="Identifier (typically an orcid.org ID)"
    )
    image: Optional[AnyHttpUrl] = Field(
        None,
        title="Image URL",
    )
    telephone: Optional[str] = Field(
        None,
        title="Telephone",
    )
    url: Optional[AnyHttpUrl] = Field(
        None,
        title="URL",
    )


class Organization(Creator):
    class_: str = Field(
        "Organization",
        const=True,
        alias="class",
    )


class Person(Creator):
    class_: str = Field(
        "Person",
        const=True,
        alias="class",
    )
    family_name: Optional[str] = Field(
        None,
        alias="familyName",
        title="Family Name",
    )
    givenName: Optional[str] = Field(
        None,
        alias="givenName",
        title="Given Name",
    )
    honorific_prefix: Optional[str] = Field(
        None,
        alias="honorificPrefix",
        title="Honorific Prefix",
        description="Honorific Prefix (e.g. Dr/Mrs/Mr)",
    )
    honorific_suffix: Optional[str] = Field(
        None,
        alias="honorificSuffix",
        title="Honorific Suffix",
        description="Honorific Suffix (e.g. M.D.)"
    )
    job_title: Optional[str] = Field(
        None,
        alias="jobTitle",
        title="Job Title",
    )


class StoredWorkflowDetailed(StoredWorkflowSummary):
    annotation: Optional[str] = AnnotationField  # Inconsistency? See comment on StoredWorkflowSummary.annotations
    license: Optional[str] = Field(
        None,
        title="License",
        description="SPDX Identifier of the license associated with this workflow."
    )
    version: int = Field(
        ...,
        title="Version",
        description="The version of the workflow represented by an incremental number."
    )
    inputs: Dict[int, WorkflowInput] = Field(
        {},
        title="Inputs",
        description="A dictionary containing information about all the inputs of the workflow."
    )
    creator: Optional[List[Union[Person, Organization]]] = Field(
        None,
        title="Creator",
        description=(
            "Additional information about the creator (or multiple creators) of this workflow."
        )
    )
    steps: Dict[int,
        Union[
            InputDataStep,
            InputDataCollectionStep,
            InputParameterStep,
            PauseStep,
            ToolStep,
            SubworkflowStep,
        ]
    ] = Field(
        {},
        title="Steps",
        description="A dictionary with information about all the steps of the workflow."
    )


class Input(BaseModel):
    name: str = Field(
        ...,
        title="Name",
        description="The name of the input."
    )
    description: str = Field(
        ...,
        title="Description",
        description="The annotation or description of the input."

    )


class Output(BaseModel):
    name: str = Field(
        ...,
        title="Name",
        description="The name of the output."
    )
    type: str = Field(
        ...,
        title="Type",
        description="The extension or type of output."

    )


class InputConnection(BaseModel):
    id: int = Field(
        ...,
        title="ID",
        description="The identifier of the input."
    )
    output_name: str = Field(
        ...,
        title="Output Name",
        description="The name assigned to the output.",
    )
    input_subworkflow_step_id: Optional[int] = Field(
        None,
        title="Input Subworkflow Step ID",
        description="TODO",
    )


class WorkflowStepLayoutPosition(BaseModel):
    """Position and dimensions of the workflow step represented by a box on the graph."""
    bottom: int = Field(
        ...,
        title="Bottom",
        description="Position in pixels of the bottom of the box."
    )
    top: int = Field(
        ...,
        title="Top",
        description="Position in pixels of the top of the box."
    )
    left: int = Field(
        ...,
        title="Left",
        description="Left margin or left-most position of the box."
    )
    right: int = Field(
        ...,
        title="Right",
        description="Right margin or right-most position of the box."
    )
    x: int = Field(
        ...,
        title="X",
        description="Horizontal pixel coordinate of the top right corner of the box."
    )
    y: int = Field(
        ...,
        title="Y",
        description="Vertical pixel coordinate of the top right corner of the box."
    )
    height: int = Field(
        ...,
        title="Height",
        description="Height of the box in pixels."
    )
    width: int = Field(
        ...,
        title="Width",
        description="Width of the box in pixels."
    )


class WorkflowStepToExportBase(BaseModel):
    id: int = Field(
        ...,
        title="ID",
        description="The identifier of the step. It matches the index order of the step inside the workflow."
    )
    type: str = Field(
        ...,
        title="Type",
        description="The type of workflow module."
    )
    name: str = Field(
        ...,
        title="Name",
        description="The descriptive name of the module or step."
    )
    annotation: Optional[str] = AnnotationField
    tool_id: Optional[str] = Field(  # Duplicate of `content_id` or viceversa?
        None,
        title="Tool ID",
        description="The unique name of the tool associated with this step."
    )
    uuid: UUID4 = Field(
        ...,
        title="UUID",
        description="Universal unique identifier of the workflow.",
    )
    label: Optional[str] = Field(
        None,
        title="Label",
    )
    inputs: List[Input] = Field(
        ...,
        title="Inputs",
        description="TODO",
    )
    outputs: List[Output] = Field(
        ...,
        title="Outputs",
        description="TODO",
    )
    input_connections: Dict[str, InputConnection] = Field(
        {},
        title="Input Connections",
        description="TODO",
    )
    position: WorkflowStepLayoutPosition = Field(
        ...,
        title="Position",
        description="Layout position of this step in the graph",
    )
    workflow_outputs: List[WorkflowOutput] = Field(
        [],
        title="Workflow Outputs",
        description="The version of the tool associated with this step."
    )


class WorkflowStepToExport(WorkflowStepToExportBase):
    content_id: Optional[str] = Field(  # Duplicate of `tool_id` or viceversa?
        None,
        title="Content ID",
        description="TODO"
    )
    tool_version: Optional[str] = Field(
        None,
        title="Tool Version",
        description="The version of the tool associated with this step."
    )
    tool_state: Json = Field(
        ...,
        title="Tool State",
        description="JSON string containing the serialized representation of the persistable state of the step.",
    )
    errors: Optional[str] = Field(
        None,
        title="Errors",
        description="An message indicating possible errors in the step.",
    )


class ToolShedRepositorySummary(BaseModel):
    name: str = Field(
        ...,
        title="Name",
        description="The name of the repository.",
    )
    owner: str = Field(
        ...,
        title="Owner",
        description="The owner of the repository.",
    )
    changeset_revision: str = Field(
        ...,
        title="Changeset Revision",
        description="TODO",
    )
    tool_shed: str = Field(
        ...,
        title="Tool Shed",
        description="The Tool Shed base URL.",
    )


class PostJobAction(BaseModel):
    action_type: str = Field(
        ...,
        title="Action Type",
        description="The type of action to run.",
    )
    output_name: str = Field(
        ...,
        title="Output Name",
        description="The name of the output that will be affected by the action.",
    )
    action_arguments: Dict[str, Any] = Field(
        ...,
        title="Action Arguments",
        description="Any additional arguments needed by the action.",
    )


class WorkflowToolStepToExport(WorkflowStepToExportBase):
    tool_shed_repository: ToolShedRepositorySummary = Field(
        ...,
        title="Tool Shed Repository",
        description="Information about the origin repository of this tool."
    )
    post_job_actions: Dict[str, PostJobAction] = Field(
        ...,
        title="Post-job Actions",
        description="Set of actions that will be run when the job finish."
    )


class SubworkflowStepToExport(WorkflowStepToExportBase):
    subworkflow: 'WorkflowToExport' = Field(
        ...,
        title="Subworkflow",
        description="Full information about the subworkflow associated with this step."
    )


class WorkflowToExport(BaseModel):
    a_galaxy_workflow: str = Field(  # Is this meant to be a bool instead?
        "true",
        title="Galaxy Workflow",
        description="Whether this workflow is a Galaxy Workflow."
    )
    format_version: str = Field(
        "0.1",
        alias="format-version",  # why this field uses `-` instead of `_`?
        title="Galaxy Workflow",
        description="Whether this workflow is a Galaxy Workflow."
    )
    name: str = Field(
        ...,
        title="Name",
        description="The name of the workflow."
    )
    annotation: Optional[str] = AnnotationField
    tags: TagCollection
    uuid: Optional[UUID4] = Field(
        None,
        title="UUID",
        description="Universal unique identifier of the workflow.",
    )
    creator: Optional[List[Union[Person, Organization]]] = Field(
        None,
        title="Creator",
        description=(
            "Additional information about the creator (or multiple creators) of this workflow."
        )
    )
    license: Optional[str] = Field(
        None,
        title="License",
        description="SPDX Identifier of the license associated with this workflow."
    )
    version: int = Field(
        ...,
        title="Version",
        description="The version of the workflow represented by an incremental number."
    )
    steps: Dict[int, Union[SubworkflowStepToExport, WorkflowToolStepToExport, WorkflowStepToExport]] = Field(
        {},
        title="Steps",
        description="A dictionary with information about all the steps of the workflow."
    )


# Roles -----------------------------------------------------------------

RoleIdField = Field(title="ID", description="Encoded ID of the role")
RoleNameField = Field(title="Name", description="Name of the role")
RoleDescriptionField = Field(title="Description", description="Description of the role")


class BasicRoleModel(BaseModel):
    id: EncodedDatabaseIdField = RoleIdField
    name: str = RoleNameField
    type: str = Field(title="Type", description="Type or category of the role")


class RoleModel(BasicRoleModel):
    description: Optional[str] = RoleDescriptionField
    url: str = Field(title="URL", description="URL for the role")
    model_class: str = ModelClassField("Role")


class RoleDefinitionModel(BaseModel):
    name: str = RoleNameField
    description: str = RoleDescriptionField
    user_ids: Optional[List[EncodedDatabaseIdField]] = Field(title="User IDs", default=[])
    group_ids: Optional[List[EncodedDatabaseIdField]] = Field(title="Group IDs", default=[])


class RoleListModel(BaseModel):
    __root__: List[RoleModel]


# The tuple should probably be another proper model instead?
# Keeping it as a Tuple for now for backward compatibility
RoleNameIdTuple = Tuple[str, EncodedDatabaseIdField]

# Group_Roles -----------------------------------------------------------------


class GroupRoleModel(BaseModel):
    id: EncodedDatabaseIdField = RoleIdField
    name: str = RoleNameField
    url: RelativeUrl = RelativeUrlField


class GroupRoleListModel(BaseModel):
    __root__: List[GroupRoleModel]

# Libraries -----------------------------------------------------------------


class LibraryPermissionScope(str, Enum):
    current = "current"
    available = "available"


class LibraryLegacySummary(BaseModel):
    model_class: str = ModelClassField("Library")
    id: EncodedDatabaseIdField = Field(
        ...,
        title="ID",
        description="Encoded ID of the Library.",
    )
    name: str = Field(
        ...,
        title="Name",
        description="The name of the Library.",
    )
    description: Optional[str] = Field(
        "",
        title="Description",
        description="A detailed description of the Library.",
    )
    synopsis: Optional[str] = Field(
        None,
        title="Description",
        description="A short text describing the contents of the Library.",
    )
    root_folder_id: EncodedDatabaseIdField = Field(
        ...,
        title="Root Folder ID",
        description="Encoded ID of the Library's base folder.",
    )
    create_time: datetime = Field(
        ...,
        title="Create Time",
        description="The time and date this item was created.",
    )
    deleted: bool = Field(
        ...,
        title="Deleted",
        description="Whether this Library has been deleted.",
    )


class LibrarySummary(LibraryLegacySummary):
    create_time_pretty: str = Field(  # This is somewhat redundant, maybe the client can do this with `create_time`?
        ...,
        title="Create Time Pretty",
        description="Nice time representation of the creation date.",
        example="2 months ago",
    )
    public: bool = Field(
        ...,
        title="Public",
        description="Whether this Library has been deleted.",
    )
    can_user_add: bool = Field(
        ...,
        title="Can User Add",
        description="Whether the current user can add contents to this Library.",
    )
    can_user_modify: bool = Field(
        ...,
        title="Can User Modify",
        description="Whether the current user can modify this Library.",
    )
    can_user_manage: bool = Field(
        ...,
        title="Can User Manage",
        description="Whether the current user can manage the Library and its contents.",
    )


class LibrarySummaryList(BaseModel):
    __root__: List[LibrarySummary] = Field(
        default=[],
        title='List with summary information of Libraries.',
    )


class CreateLibraryPayload(BaseModel):
    name: str = Field(
        ...,
        title="Name",
        description="The name of the Library.",
    )
    description: Optional[str] = Field(
        "",
        title="Description",
        description="A detailed description of the Library.",
    )
    synopsis: Optional[str] = Field(
        "",
        title="Synopsis",
        description="A short text describing the contents of the Library.",
    )


class UpdateLibraryPayload(BaseModel):
    name: Optional[str] = Field(
        None,
        title="Name",
        description="The new name of the Library. Leave unset to keep the existing.",
    )
    description: Optional[str] = Field(
        None,
        title="Description",
        description="A detailed description of the Library. Leave unset to keep the existing.",
    )
    synopsis: Optional[str] = Field(
        None,
        title="Synopsis",
        description="A short text describing the contents of the Library. Leave unset to keep the existing.",
    )


class DeleteLibraryPayload(BaseModel):
    undelete: bool = Field(
        ...,
        title="Undelete",
        description="Whether to restore this previously deleted library.",
    )


class LibraryCurrentPermissions(BaseModel):
    access_library_role_list: List[RoleNameIdTuple] = Field(
        ...,
        title="Access Role List",
        description="A list containing pairs of role names and corresponding encoded IDs which have access to the Library.",
    )
    modify_library_role_list: List[RoleNameIdTuple] = Field(
        ...,
        title="Modify Role List",
        description="A list containing pairs of role names and corresponding encoded IDs which can modify the Library.",
    )
    manage_library_role_list: List[RoleNameIdTuple] = Field(
        ...,
        title="Manage Role List",
        description="A list containing pairs of role names and corresponding encoded IDs which can manage the Library.",
    )
    add_library_item_role_list: List[RoleNameIdTuple] = Field(
        ...,
        title="Add Role List",
        description="A list containing pairs of role names and corresponding encoded IDs which can add items to the Library.",
    )


RoleIdList = Union[List[EncodedDatabaseIdField], EncodedDatabaseIdField]  # Should we support just List[EncodedDatabaseIdField] in the future?


class LegacyLibraryPermissionsPayload(BaseModel):
    LIBRARY_ACCESS_in: Optional[RoleIdList] = Field(
        [],
        title="Access IDs",
        description="A list of role encoded IDs defining roles that should have access permission on the library.",
    )
    LIBRARY_MODIFY_in: Optional[RoleIdList] = Field(
        [],
        title="Add IDs",
        description="A list of role encoded IDs defining roles that should be able to add items to the library.",
    )
    LIBRARY_ADD_in: Optional[RoleIdList] = Field(
        [],
        title="Manage IDs",
        description="A list of role encoded IDs defining roles that should have manage permission on the library.",
    )
    LIBRARY_MANAGE_in: Optional[RoleIdList] = Field(
        [],
        title="Modify IDs",
        description="A list of role encoded IDs defining roles that should have modify permission on the library.",
    )


class LibraryPermissionAction(str, Enum):
    set_permissions = "set_permissions"
    remove_restrictions = "remove_restrictions"  # name inconsistency? should be `make_public`?


class DatasetPermissionAction(str, Enum):
    set_permissions = "set_permissions"
    make_private = "make_private"
    remove_restrictions = "remove_restrictions"


class LibraryPermissionsPayloadBase(Model):
    add_ids: Optional[RoleIdList] = Field(
        [],
        alias="add_ids[]",
        title="Add IDs",
        description="A list of role encoded IDs defining roles that should be able to add items to the library.",
    )
    manage_ids: Optional[RoleIdList] = Field(
        [],
        alias="manage_ids[]",
        title="Manage IDs",
        description="A list of role encoded IDs defining roles that should have manage permission on the library.",
    )
    modify_ids: Optional[RoleIdList] = Field(
        [],
        alias="modify_ids[]",
        title="Modify IDs",
        description="A list of role encoded IDs defining roles that should have modify permission on the library.",
    )


class LibraryPermissionsPayload(LibraryPermissionsPayloadBase):
    action: Optional[LibraryPermissionAction] = Field(
        ...,
        title="Action",
        description="Indicates what action should be performed on the Library.",
    )
    access_ids: Optional[RoleIdList] = Field(
        [],
        alias="access_ids[]",  # Added for backward compatibility but it looks really ugly...
        title="Access IDs",
        description="A list of role encoded IDs defining roles that should have access permission on the library.",
    )


# Library Folders -----------------------------------------------------------------

class LibraryFolderPermissionAction(str, Enum):
    set_permissions = "set_permissions"


FolderNameField: str = Field(
    ...,
    title="Name",
    description="The name of the library folder.",
)
FolderDescriptionField: Optional[str] = Field(
    "",
    title="Description",
    description="A detailed description of the library folder.",
)


class LibraryFolderPermissionsPayload(LibraryPermissionsPayloadBase):
    action: Optional[LibraryFolderPermissionAction] = Field(
        None,
        title="Action",
        description="Indicates what action should be performed on the library folder.",
    )


class LibraryFolderDetails(BaseModel):
    model_class: str = ModelClassField("LibraryFolder")
    id: EncodedDatabaseIdField = Field(
        ...,
        title="ID",
        description="Encoded ID of the library folder.",
    )
    name: str = FolderNameField
    description: Optional[str] = FolderDescriptionField
    item_count: int = Field(
        ...,
        title="Item Count",
        description="A detailed description of the library folder.",
    )
    parent_library_id: EncodedDatabaseIdField = Field(
        ...,
        title="Parent Library ID",
        description="Encoded ID of the Library this folder belongs to.",
    )
    parent_id: Optional[EncodedDatabaseIdField] = Field(
        None,
        title="Parent Folder ID",
        description="Encoded ID of the parent folder. Empty if it's the root folder.",
    )
    genome_build: Optional[str] = GenomeBuildField
    update_time: datetime = UpdateTimeField
    deleted: bool = Field(
        ...,
        title="Deleted",
        description="Whether this folder is marked as deleted.",
    )
    library_path: List[str] = Field(
        [],
        title="Path",
        description="The list of folder names composing the path to this folder.",
    )


class CreateLibraryFolderPayload(BaseModel):
    name: str = FolderNameField
    description: Optional[str] = FolderDescriptionField


class UpdateLibraryFolderPayload(BaseModel):
    name: Optional[str] = Field(
        default=None,
        title="Name",
        description="The new name of the library folder.",
    )
    description: Optional[str] = Field(
        default=None,
        title="Description",
        description="The new description of the library folder.",
    )


class LibraryAvailablePermissions(BaseModel):
    roles: List[BasicRoleModel] = Field(
        ...,
        title="Roles",
        description="A list available roles that can be assigned to a particular permission.",
    )
    page: int = Field(
        ...,
        title="Page",
        description="Current page .",
    )
    page_limit: int = Field(
        ...,
        title="Page Limit",
        description="Maximum number of items per page.",
    )
    total: int = Field(
        ...,
        title="Total",
        description="Total number of items",
    )


class LibraryFolderCurrentPermissions(BaseModel):
    modify_folder_role_list: List[RoleNameIdTuple] = Field(
        ...,
        title="Modify Role List",
        description="A list containing pairs of role names and corresponding encoded IDs which can modify the Library folder.",
    )
    manage_folder_role_list: List[RoleNameIdTuple] = Field(
        ...,
        title="Manage Role List",
        description="A list containing pairs of role names and corresponding encoded IDs which can manage the Library folder.",
    )
    add_library_item_role_list: List[RoleNameIdTuple] = Field(
        ...,
        title="Add Role List",
        description="A list containing pairs of role names and corresponding encoded IDs which can add items to the Library folder.",
    )


class DatasetAssociationRoles(Model):
    access_dataset_roles: List[RoleNameIdTuple] = Field(
        default=[],
        title="Access Roles",
        description=(
            "A list of roles that can access the dataset. "
            "The user has to **have all these roles** in order to access this dataset. "
            "Users without access permission **cannot** have other permissions on this dataset. "
            "If there are no access roles set on the dataset it is considered **unrestricted**."
        ),
    )
    manage_dataset_roles: List[RoleNameIdTuple] = Field(
        default=[],
        title="Manage Roles",
        description=(
            "A list of roles that can manage permissions on the dataset. "
            "Users with **any** of these roles can manage permissions of this dataset. "
            "If you remove yourself you will lose the ability to manage this dataset unless you are an admin."
        ),
    )
    modify_item_roles: List[RoleNameIdTuple] = Field(
        default=[],
        title="Modify Roles",
        description=(
            "A list of roles that can modify the library item. This is a library related permission. "
            "User with **any** of these roles can modify name, metadata, and other information about this library item."
        ),
    )


class UpdateDatasetPermissionsPayload(Model):
    action: Optional[DatasetPermissionAction] = Field(
        ...,
        title="Action",
        description="Indicates what action should be performed on the dataset.",
    )
    access_ids: Optional[RoleIdList] = Field(
        [],
        alias="access_ids[]",  # Added for backward compatibility but it looks really ugly...
        title="Access IDs",
        description="A list of role encoded IDs defining roles that should have access permission on the dataset.",
    )
    manage_ids: Optional[RoleIdList] = Field(
        [],
        alias="manage_ids[]",
        title="Manage IDs",
        description="A list of role encoded IDs defining roles that should have manage permission on the dataset.",
    )
    modify_ids: Optional[RoleIdList] = Field(
        [],
        alias="modify_ids[]",
        title="Modify IDs",
        description="A list of role encoded IDs defining roles that should have modify permission on the dataset.",
    )


class DeleteHDCAResult(Model):
    id: EncodedDatabaseIdField = Field(
        ...,
        title="ID",
        description="The encoded ID of the collection.",
    )
    deleted: bool = Field(
        ...,
        title="Deleted",
        description="True if the collection was successfully deleted.",
    )
