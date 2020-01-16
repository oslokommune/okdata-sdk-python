import json
from dataclasses import dataclass

from origo.pipelines.resources.pipeline_base import PipelineBase
from origo.pipelines.resources.pipeline_input import PipelineInput
from origo.sdk import SDK


@dataclass
class PipelineInstance(PipelineBase):
    """A Pipeline Instance resource in pipeline-api

    Pipeline Instance contains info used with a Pipeline resource to create input for an AWS state-machine.

    Attributes:
        sdk: An instance of the SDK
        id: unique id for this resource
        datasetUri: Must conform to the following pattern: `output/{dataset_id}/{version}`.
            Defines what dataset + version this pipeline instance should result in. e.g. Running the pipeline instance
            should create a new edition in this dataset + version combination.
        pipelineArn: What Pipeline should be used.
        schemaId: Id for a schema. Used to validate the input or output.
            TODO: For now it's up to the pipeline to include a validation step. So this might not be in use even if supplied.
        transformation: object Transformation for the given Pipeline. Should include config for each step in
            the state-machine if needed. Should be validated against Pipeline.transformation_schema
        useLatestEdition: bool Whether or not to create a new edition or use the latest edition when running the pipeline.
    """

    __resource_name__ = "pipeline-instances"

    @property
    def id(self):
        return self._id

    def __init__(
        self,
        sdk: SDK,
        id: str,
        datasetUri: str,
        pipelineArn: str,
        schemaId: str,
        transformation: object,
        useLatestEdition: bool,
    ):
        self.sdk = sdk
        self._id = id
        self.datasetUri = datasetUri
        self.pipelineArn = pipelineArn
        self.schemaId = schemaId
        self.transformation = transformation
        self.useLatestEdition = useLatestEdition

    @property
    def __dict__(self):
        return {
            "id": self.id,
            "datasetUri": self.datasetUri,
            "pipelineArn": self.pipelineArn,
            "schemaId": self.schemaId,
            "transformation": self.transformation,
            "useLatestEdition": self.useLatestEdition,
        }

    def __repr__(self):
        return json.dumps(self.__dict__)

    def exists(self):
        return self._exists(self.sdk, self.id)

    def delete(self):
        return self._delete(self.sdk, self.id)

    def get_inputs(self):
        url = self.sdk.config.get("pipelineUrl")
        result = self.sdk.get(
            url=f"{url}/{self.__resource_name__}/{self.id}/inputs"
        ).json()
        inputs = [PipelineInput.from_dict(self.sdk, input) for input in result]
        return inputs

    def get_input(self, dataset, version):
        url = self.sdk.config.get("pipelineUrl")
        result = self.sdk.get(
            url=f"{url}/{self.__resource_name__}/{self.id}/inputs/{dataset}/{version}"
        ).text.strip("'")
        return PipelineInput.from_dict(self.sdk, result)
