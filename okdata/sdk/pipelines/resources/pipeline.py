import json
from typing import List

from requests import HTTPError

from okdata.sdk.pipelines.resources.pipeline_base import PipelineBase
from okdata.sdk.pipelines.resources.pipeline_instance import PipelineInstance
from okdata.sdk import SDK


class Pipeline(PipelineBase):
    """A Pipeline resource in pipeline-api

    Pipeline contains info about what and how to run a step-functions machine in aws.
    With useful crud functions

    Attributes:
        sdk: An instance of the SDK
        arn: A state-machine arn (step-functions)
        template (str): A template for generating step-functions input for the state-machine when combined with
            PipelineInstance's 'transformation'.
        transformation_schema (str): A schema used to validate template input. (Validate PipelineInstance's 'transformation')
    """

    __resource_name__ = "pipelines"

    @property
    def arn(self):
        return self._arn

    def __init__(self, sdk: SDK, arn: str, template: str, transformation_schema: str):
        self.sdk = sdk
        self._arn = arn
        self.template = template
        self.transformation_schema = transformation_schema

    @property
    def __dict__(self):
        return {
            "arn": self.arn,
            "template": self.template,
            "transformation_schema": self.transformation_schema,
        }

    def __repr__(self):
        return json.dumps(self.__dict__)

    def list_instances(self):
        base_url = self.sdk.config.get("pipelineUrl")
        url = f"{base_url}/{PipelineInstance.__resource_name__}"
        try:
            result: List[dict] = self.sdk.get(
                url, params={"pipeline-arn": self.arn}
            ).json()
            instances = list(
                map(
                    lambda instance: PipelineInstance.from_dict(self.sdk, instance),
                    result,
                )
            )
            return instances, None
        except HTTPError as he:
            return [], he

    def exists(self):
        return self.from_id(self.sdk, self.arn)

    def delete(self):
        return self._delete(self.sdk, self.arn)
