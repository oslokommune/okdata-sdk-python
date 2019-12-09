import json
from origo.pipelines.client import PipelineApiClient
from origo.pipelines.resources.pipeline_instance import PipelineInstance
from tests.origio.conftest import create_pipeline_instance_request


def test_create_pipeline_instance_from_json(sdk, mock_create_pipeline_instance):
    instance = PipelineInstance.from_json(sdk, create_pipeline_instance_request())
    response, error = instance.create()
    assert error is None
    assert response == '"pipeline-instance-id"'


def test_create_pipeline_instance_basic(sdk, mock_create_pipeline_instance):
    instance_input = json.loads(create_pipeline_instance_request())
    instance = PipelineInstance(sdk, **instance_input)
    response, error = instance.create()
    assert error is None
    assert response == '"pipeline-instance-id"'


def test_create_pipeline_instance_from_dict(sdk, mock_create_pipeline_instance):
    instance_input = json.loads(create_pipeline_instance_request())
    instance = PipelineInstance.from_dict(sdk, instance_input)
    response, error = instance.create()
    assert error is None
    assert response == '"pipeline-instance-id"'


def test_get_pipeline_instance(mock_get_pipeline_instance):
    client = PipelineApiClient()
    instance = client.fetch(PipelineInstance, "pipeline-instance-id")
    expected = json.loads(create_pipeline_instance_request())
    assert instance.transformation == expected["transformation"]
