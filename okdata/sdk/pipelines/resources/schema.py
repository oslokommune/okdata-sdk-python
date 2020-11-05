import json

from okdata.sdk.pipelines.resources.pipeline_base import PipelineBase
from okdata.sdk import SDK


class Schema(PipelineBase):
    """A Schema resource in pipeline-api

    Schema contains info about the structure of the data in a dataset.

    Attributes:
        sdk: An instance of the SDK
        id: str unique id for this resource
        schema: str JSONSchema for the dataset.
    """

    __resource_name__ = "schemas"

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return "schema"

    def __init__(self, sdk: SDK, id: str, schema: str, type: str = "schema"):
        self.sdk = sdk
        self._id = id
        self.schema = schema

    @property
    def __dict__(self):
        return {"id": self.id, "schema": self.schema, "type": self.type}

    def __repr__(self):
        return json.dumps(self.__dict__)

    def exists(self):
        return self._exists(self.sdk, self.id)

    def delete(self):
        return self._delete(self.sdk, self.id)
