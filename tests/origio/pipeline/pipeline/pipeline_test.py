import json
from jsonschema import ValidationError
from origo.pipelines.client import PipelineApiClient
from origo.pipelines.resources.pipeline import Pipeline
from origo.pipelines.resources.pipeline_instance import PipelineInstance
from tests.origio.conftest import create_pipeline_request


def test_pipeline_valid(sdk, ok_pipeline):
    pipeline = Pipeline.from_json(sdk=sdk, resource=ok_pipeline)
    valid, error = pipeline.validate()
    assert error is None
    assert valid


def test_pipeline_not_valid(sdk, ok_pipeline):
    invalid = json.loads(ok_pipeline)
    invalid["arn"] = "wrong"
    pipeline_invalid = Pipeline.from_json(sdk=sdk, resource=json.dumps(invalid))
    valid, error = pipeline_invalid.validate()
    assert not valid
    assert type(error) is ValidationError


def test_create_pipeline_201(sdk, ok_pipeline, mock_create_pipeline):
    pipeline = Pipeline.from_json(sdk=sdk, resource=ok_pipeline)
    valid, _ = pipeline.validate()
    assert valid
    response, error = pipeline.create()
    assert error is None
    assert (
        response
        == '"arn:aws:states:eu-west-1:123456789101:stateMachine:test-pipeline-excel-to-csv"'
    )


def test_create_pipeline_500(sdk, ok_pipeline, mock_create_pipeline_500):
    pipeline = Pipeline.from_json(sdk=sdk, resource=ok_pipeline)
    valid, _ = pipeline.validate()
    assert valid
    response, error = pipeline.create()
    assert error.response.status_code == 500
    assert response is None


def test_create_pipeline_400(sdk, ok_pipeline, mock_create_pipeline_404):
    pipeline = Pipeline.from_json(sdk=sdk, resource=ok_pipeline)
    valid, _ = pipeline.validate()
    assert valid
    response, error = pipeline.create()
    assert error.response.status_code == 404
    assert response is None


def test_list_instances_for_pipeline(sdk, ok_pipeline, mock_list_instances):
    pipeline = Pipeline.from_json(sdk=sdk, resource=ok_pipeline)
    instances, error = pipeline.list_instances()
    assert error is None
    assert len(instances) == 2
    assert type(instances[0]) == PipelineInstance


def test_client_exists_check(mock_get_pipeline):
    sdk = PipelineApiClient()
    response = create_pipeline_request()
    arn = json.loads(response)["arn"]
    r = sdk.exists(Pipeline, arn)
    assert r


def test_delete_pipeline(mock_get_pipeline, mock_delete_pipeline):
    sdk = PipelineApiClient()
    response = create_pipeline_request()
    arn = json.loads(response)["arn"]
    pipeline: Pipeline = sdk.fetch(Pipeline, arn)
    pipeline.delete()
    assert mock_delete_pipeline.called


def test_update_pipeline(mock_get_pipeline, mock_delete_pipeline, mock_create_pipeline):
    sdk = PipelineApiClient()
    response = create_pipeline_request()
    arn = json.loads(response)["arn"]
    pipeline: Pipeline = sdk.fetch(Pipeline, arn)
    pipeline.transformation_schema = "blablabla"
    pipeline.update()
    assert mock_delete_pipeline.called
    assert mock_delete_pipeline.call_count == 1
    assert mock_create_pipeline.called
    assert mock_create_pipeline.call_count == 1
