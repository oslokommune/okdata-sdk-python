import json
import os
from typing import Tuple, Optional

import jsonschema  # type: ignore
from jsonschema import ValidationError, SchemaError

from okdata.sdk.pipelines.resources.pipeline_base import PipelineBase, InternalError
from okdata.sdk import SDK


class PipelineInput(PipelineBase):
    """A Pipeline Input resource in pipeline-api

    Pipeline Input contains info about which datasets should trigger a pipeline instance.

    Attributes:
        sdk: An instance of the SDK
        pipelineInstanceId: pipeline instance id
        datasetUri: Must conform to the following pattern: `input/{dataset_id}/{version}`.
           Defines which dataset should trigger the corresponding pipeline instance
        stage: string Both dataset and stage must match for the instance to trigger correctly.
    """

    @property
    def __resource_name__(self):
        return f"pipeline-instances/{self.pipelineInstanceId}/inputs"

    def __init__(self, sdk: SDK, datasetUri: str, stage: str, pipelineInstanceId: str):
        self.sdk = sdk
        self.pipelineInstanceId = pipelineInstanceId
        self.datasetUri = datasetUri
        self.stage = stage

    @classmethod
    def from_id(cls, sdk: SDK, id: str):
        raise NotImplementedError

    @classmethod
    def _exists(cls, sdk, id):
        raise NotImplementedError

    @classmethod
    def _delete(cls, sdk: SDK, id: str):
        raise NotImplementedError

    def validate(self) -> Tuple[bool, Optional[ValidationError]]:
        path = os.path.dirname(__file__)
        with open(f"{path}/schemas/pipeline-inputs.json") as f:
            try:
                jsonschema.validate(self.__dict__, json.loads(f.read()))
                return True, None
            except SchemaError:
                # TODO: Logging
                raise InternalError
            except ValidationError as ve:
                # TODO: Logging
                return False, ve

    @property
    def __dict__(self):
        return {
            "datasetUri": self.datasetUri,
            "stage": self.stage,
            "pipelineInstanceId": self.pipelineInstanceId,
        }

    def __repr__(self):
        return json.dumps(self.__dict__)

    def exists(self):
        return self._exists(self.sdk, self.pipelineInstanceId)

    def delete(self):
        dataset = self.datasetUri.split("/")[1]
        version = self.datasetUri.split("/")[2]
        url = self.sdk.config.get("pipelineUrl")
        result = self.sdk.delete(
            url=f"{url}/{self.__resource_name__}/{dataset}/{version}"
        ).text.strip('"')
        return result
