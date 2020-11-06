import json
from okdata.sdk.pipelines.client import PipelineApiClient
from okdata.sdk.pipelines.resources.pipeline_input import PipelineInput
from tests.conftest import create_pipeline_input_request


def test_create_pipeline_input_from_json(sdk, mock_create_pipeline_input):
    instance = PipelineInput.from_json(sdk, create_pipeline_input_request())
    response, error = instance.create()
    assert error is None
    assert response == '"pipeline-instance-id"'


def test_create_pipeline_input_basic(sdk, mock_create_pipeline_input):
    instance_input = json.loads(create_pipeline_input_request())
    instance = PipelineInput(sdk, **instance_input)
    response, error = instance.create()
    assert error is None
    assert response == '"pipeline-instance-id"'


def test_create_pipeline_input_from_dict(sdk, mock_create_pipeline_input):
    instance_input = json.loads(create_pipeline_input_request())
    instance = PipelineInput.from_dict(sdk, instance_input)
    response, error = instance.create()
    assert error is None
    assert response == '"pipeline-instance-id"'


def test_get_pipeline_input(mock_get_pipeline_inputs):
    client = PipelineApiClient()
    result = client.get_pipeline_inputs("pipeline-instance-id")
    assert len(result) > 0
    assert mock_get_pipeline_inputs.called


def test_delete_pipeline_input(mock_delete_pipeline_input):
    client = PipelineApiClient()
    result = client.delete_pipeline_input("pipeline-instance-id", "dataset-id", "1")
    assert len(result) > 0
    assert mock_delete_pipeline_input.called
