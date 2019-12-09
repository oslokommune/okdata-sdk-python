from typing import Type

from origo.pipelines.resources.pipeline_base import PipelineBase
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
