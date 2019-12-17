import json

import pytest
from requests import HTTPError

from origo.pipelines.client import PipelineApiClient


def test_pipeline_helpers(
    mock_get_pipeline, mock_create_pipeline_500, mock_delete_pipeline, ok_pipeline
):
    sdk = PipelineApiClient()
    with pytest.raises(HTTPError):
        sdk.create_pipeline(json.loads(ok_pipeline))
        assert mock_create_pipeline_500.called

    arn = json.loads(ok_pipeline)["arn"]
    sdk.get_pipeline(arn)
    assert mock_get_pipeline.called

    sdk.delete_pipeline(arn)
    assert mock_delete_pipeline.called


def test_pipeline_instance_helpers(
    mock_get_pipeline_instance,
    mock_create_pipeline_instance,
    mock_delete_pipeline_instance,
    ok_pipeline_instance,
):
    sdk = PipelineApiClient()
    id = sdk.create_pipeline_instance(json.loads(ok_pipeline_instance))
    id = id.replace('"', "")
    assert mock_create_pipeline_instance.called

    sdk.get_pipeline_instance(id)
    assert mock_get_pipeline_instance.called

    sdk.delete_pipeline_instance(id)
    assert mock_delete_pipeline_instance.called
