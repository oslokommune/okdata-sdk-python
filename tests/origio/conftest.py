import json
import os
import re
from urllib.parse import urlencode

import pytest

from origo.config import ORIGO_CONFIG
from origo.pipelines.resources.pipeline_instance import PipelineInstance
from origo.sdk import SDK
from tests.origio.test_utils import well_known_response, client_credentials_response


def read_pipeline_file(filename):
    path = os.path.dirname(__file__)
    with open(f"{path}/pipeline/{filename}") as f:
        return f.read()


def create_pipeline_reponse():
    return read_pipeline_file("pipeline/response.json")


def create_pipeline_request():
    return read_pipeline_file("pipeline/request.json")


def create_pipeline_instance_reponse():
    return read_pipeline_file("pipeline_instance/response.json")


def create_pipeline_instance_request():
    return read_pipeline_file("pipeline_instance/request.json")


@pytest.fixture()
def ok_pipeline():
    return create_pipeline_request()


@pytest.fixture()
def ok_pipeline_instance():
    return create_pipeline_instance_request()


@pytest.fixture(autouse=True)
def mock_well_known(requests_mock):
    requests_mock.register_uri(
        "GET",
        "https://login-test.oslo.kommune.no/auth/realms/api-catalog/.well-known/openid-configuration",
        text=json.dumps(well_known_response),
        status_code=200,
    )


@pytest.fixture(autouse=True)
def mock_token_endpoint(requests_mock):
    requests_mock.register_uri(
        "POST",
        re.compile(".*/token$"),
        text=json.dumps(client_credentials_response),
        status_code=200,
    )


@pytest.fixture(scope="function", autouse=True)
def mock_home_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))


@pytest.fixture()
def sdk():
    sdk = SDK()
    sdk.login()
    return sdk


@pytest.fixture()
def mock_create_pipeline(requests_mock):
    pipeline_url = ORIGO_CONFIG["dev"]["pipelineUrl"]
    response = create_pipeline_reponse()
    return requests_mock.register_uri(
        "POST", url=f"{pipeline_url}/pipelines", text=response, status_code=201,
    )


@pytest.fixture()
def mock_delete_pipeline(requests_mock):
    pipeline_url = ORIGO_CONFIG["dev"]["pipelineUrl"]
    response = create_pipeline_request()
    arn = json.loads(response)["arn"]
    return requests_mock.register_uri(
        "DELETE",
        url=f"{pipeline_url}/pipelines/{arn}",
        text=f"Deleted pipeline {arn}",
        status_code=200,
    )


@pytest.fixture()
def mock_delete_pipeline_instance(requests_mock):
    pipeline_url = ORIGO_CONFIG["dev"]["pipelineUrl"]
    response = create_pipeline_instance_request()
    arn = json.loads(response)["id"]
    return requests_mock.register_uri(
        "DELETE",
        url=f"{pipeline_url}/pipeline_instances/{arn}",
        text=f"Deleted pipeline instance {arn}",
        status_code=200,
    )


@pytest.fixture()
def mock_get_pipeline(requests_mock):
    pipeline_url = ORIGO_CONFIG["dev"]["pipelineUrl"]
    response = create_pipeline_request()
    arn = json.loads(response)["arn"]
    return requests_mock.register_uri(
        "GET", url=f"{pipeline_url}/pipelines/{arn}", text=response, status_code=200,
    )


@pytest.fixture()
def mock_create_pipeline_500(requests_mock):
    pipeline_url = ORIGO_CONFIG["dev"]["pipelineUrl"]
    response = create_pipeline_reponse()
    return requests_mock.register_uri(
        "POST", url=f"{pipeline_url}/pipelines", text=response, status_code=500,
    )


@pytest.fixture()
def mock_create_pipeline_404(requests_mock):
    pipeline_url = ORIGO_CONFIG["dev"]["pipelineUrl"]
    response = create_pipeline_reponse()
    return requests_mock.register_uri(
        "POST", url=f"{pipeline_url}/pipelines", text=response, status_code=404,
    )


@pytest.fixture()
def mock_list_instances(sdk, requests_mock):
    pipeline_url = ORIGO_CONFIG["dev"]["pipelineUrl"]
    instance = json.loads(create_pipeline_instance_request())
    instance1 = PipelineInstance.from_dict(sdk=sdk, instance_dict=instance)
    instance["id"] = "instance2"
    instance2 = PipelineInstance.from_dict(sdk=sdk, instance_dict=instance)
    response = json.dumps([instance1.__dict__, instance2.__dict__])
    url_encoded_arn = urlencode(
        {
            "pipeline-arn": "arn:aws:states:eu-west-1:123456789101:stateMachine:test-pipeline-excel-to-csv"
        }
    )
    return requests_mock.register_uri(
        "GET",
        url=f"{pipeline_url}/pipeline_instances?{url_encoded_arn}",
        text=response,
        status_code=200,
    )


@pytest.fixture()
def mock_create_pipeline_instance(requests_mock):
    pipeline_url = ORIGO_CONFIG["dev"]["pipelineUrl"]
    response = create_pipeline_instance_reponse()
    return requests_mock.register_uri(
        "POST",
        url=f"{pipeline_url}/pipeline_instances",
        text=response,
        status_code=201,
    )


@pytest.fixture()
def mock_get_pipeline_instance(requests_mock):
    pipeline_url = ORIGO_CONFIG["dev"]["pipelineUrl"]
    response = create_pipeline_instance_request()
    id = "pipeline-instance-id"
    return requests_mock.register_uri(
        "GET",
        url=f"{pipeline_url}/pipeline_instances/{id}",
        text=response,
        status_code=201,
    )
