from typing import Type, List

from origo.pipelines.resources.pipeline import Pipeline
from origo.pipelines.resources.pipeline_base import PipelineBase
from origo.pipelines.resources.pipeline_instance import PipelineInstance
from origo.sdk import SDK


class PipelineApiClient(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "pipeline-api"
        super().__init__(config, auth, env)

    def exists(self, base: Type[PipelineBase], id):
        return base._exists(self, id)

    def fetch(self, base: Type[PipelineBase], id):
        return base.from_id(self, id)

    def list(self, base: Type[PipelineBase]):
        return base.list(self)

    def get_pipelines(self) -> List[Pipeline]:
        return self.list(Pipeline)

    def get_pipeline_instances(self) -> List[PipelineInstance]:
        return self.list(PipelineInstance)

    def get_pipeline(self, arn: str) -> Pipeline:
        return self.fetch(Pipeline, arn)

    def get_pipeline_instance(self, id: str) -> PipelineInstance:
        return self.fetch(PipelineInstance, id)

    def create_pipeline(self, data: dict):
        created, error = Pipeline.from_dict(self, data).create()
        if error:
            raise error
        return created

    def create_pipeline_instance(self, data: dict):
        created, error = PipelineInstance.from_dict(self, data).create()
        if error:
            raise error
        return created

    def delete_pipeline(self, arn: str):
        return Pipeline._delete(self, arn)

    def delete_pipeline_instance(self, id: str):
        return PipelineInstance._delete(self, id)
