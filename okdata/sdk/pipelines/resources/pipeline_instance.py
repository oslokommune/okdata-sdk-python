import json

from okdata.sdk.pipelines.resources.pipeline_base import PipelineBase
from okdata.sdk.pipelines.resources.pipeline_input import PipelineInput
from okdata.sdk import SDK


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
        pipelineProcessorId: ID of the pipeline processor to use.
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
        taskConfig: object = None,
        # TODO: Remove this once all users have been updated to use
        # `pipelineProcessorId` instead.
        pipelineArn: str = None,
        # TODO: Make this required once `pipelineArn` has been phased out.
        pipelineProcessorId: str = None,
    ):
        self.sdk = sdk
        self._id = id
        self.datasetUri = datasetUri
        self.pipelineArn = pipelineArn
        self.pipelineProcessorId = pipelineProcessorId
        self.taskConfig = taskConfig

    @property
    def __dict__(self):
        dictionary = {
            "id": self.id,
            "datasetUri": self.datasetUri,
            "taskConfig": self.taskConfig,
        }
        if self.taskConfig is not None:
            dictionary["taskConfig"] = self.taskConfig
        if self.pipelineArn is not None:
            dictionary["pipelineArn"] = self.pipelineArn
        if self.pipelineProcessorId is not None:
            dictionary["pipelineProcessorId"] = self.pipelineProcessorId
        return dictionary

    @classmethod
    def from_dict(cls, sdk: SDK, instance_dict: dict):
        """Create and return a pipeline instance from a dictionary.

        Overrides the method from `PipelineBase` to be able to pick and choose
        from `instance_dict`, instead of requiring an exact match with this
        class' `___init___` parameters.
        """
        return cls(
            sdk,
            **{
                key: instance_dict[key]
                for key in [
                    "id",
                    "datasetUri",
                    "taskConfig",
                    "pipelineArn",
                    "pipelineProcessorId",
                ]
                if key in instance_dict
            },
        )

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
