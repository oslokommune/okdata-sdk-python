import os
import pytest
import json

from origo.data.data_exporter_client import DataExporterClient

data_exporter_client = DataExporterClient()

file_name = "kake.csv"
s3_key = f"procecced/raw/green/{file_name}"
download_url = "https://www.dowload-stuff.com"

dataset_id = "test-dataset"
version = 1
edition = "latest"

test_file_content = "kake;basilikum;laks;soyasaus"


def test_download_files_default_output_path(mock_home_dir, mock_http_calls):
    result = data_exporter_client.download_files(dataset_id, version, edition)
    exp_output_file_path = f"{os.environ['HOME']}/{s3_key}"
    with open(exp_output_file_path, "r") as f:
        assert str(f) == test_file_content
    assert result == {"downloaded_files": [exp_output_file_path]}


def test_download_files_alternative_output_path(mock_home_dir, mock_http_calls):
    alternative_path = "alternative/path"
    result = data_exporter_client.download_files(
        dataset_id, version, edition, output_path=alternative_path
    )
    exp_output_file_path = f"{os.environ['HOME']}/{alternative_path}/{file_name}"
    with open(exp_output_file_path, "r") as f:
        assert str(f) == test_file_content
    assert result == {"downloaded_files": [exp_output_file_path]}


@pytest.fixture(scope="function")
def mock_home_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))


def mock_http_calls(requests_mock):

    requests_mock.register_uri(
        "GET",
        f"{data_exporter_client.data_exporter_url}/{dataset_id}/{version}/{edition}",
        text=json.dumps({"key": s3_key, "url": download_url}),
        status_code=200,
    )

    requests_mock.register_uri(
        "GET", download_url, text=test_file_content, status_code=200
    )
