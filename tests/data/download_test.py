import os
import pytest
import json

from okdata.sdk.data.download import Download

file_name = "kake.csv"
s3_key = f"procecced/raw/green/{file_name}"
download_url = "https://www.dowload-stuff.com"

dataset_id = "test-dataset"
version = 1
edition = "latest"

test_file_content = "kake;basilikum;laks;soyasaus"


def test_download(mock_home_dir, mock_http_calls):
    data_downloader = Download()
    output_path = f"{os.environ['HOME']}/my/path"
    result = data_downloader.download(
        dataset_id, version, edition, output_path=output_path
    )
    exp_output_file_path = f"{output_path}/{file_name}"
    with open(exp_output_file_path, "r") as f:
        assert str(f.read()) == test_file_content
    assert result == {"files": [exp_output_file_path]}


def test_download_public(mock_home_dir, mock_http_calls_public):
    data_downloader = Download()
    data_downloader.auth.token_provider = None
    output_path = f"{os.environ['HOME']}/my/path"
    result = data_downloader.download(
        dataset_id, version, edition, output_path=output_path
    )
    exp_output_file_path = f"{output_path}/{file_name}"
    with open(exp_output_file_path, "r") as f:
        assert str(f.read()) == test_file_content
    assert result == {"files": [exp_output_file_path]}


@pytest.fixture(scope="function")
def mock_home_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))


@pytest.fixture(scope="function")
def mock_http_calls(requests_mock):
    requests_mock.register_uri(
        "GET",
        f"{Download().data_exporter_url}/{dataset_id}/{version}/{edition}",
        text=json.dumps([{"key": s3_key, "url": download_url}]),
        status_code=200,
    )

    requests_mock.register_uri(
        "GET", download_url, text=test_file_content, status_code=200
    )


@pytest.fixture(scope="function")
def mock_http_calls_public(requests_mock):
    requests_mock.register_uri(
        "GET",
        f"{Download().data_exporter_url}/public/{dataset_id}/{version}/{edition}",
        text=json.dumps([{"key": s3_key, "url": download_url}]),
        status_code=200,
    )

    requests_mock.register_uri(
        "GET", download_url, text=test_file_content, status_code=200
    )
