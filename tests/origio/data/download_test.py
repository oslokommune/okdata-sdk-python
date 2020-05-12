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


class DownloadTest:
    def test_download_files(self, mock_home_dir, mock_http_calls):
        data_exporter_client.download_files(dataset_id, version, edition)
        with open(f"{os.environ['HOME']}/{s3_key}", "r") as f:
            assert str(f) == test_file_content

        alternative_path = "alternative/path"
        data_exporter_client.download_files(
            dataset_id, version, edition, output_path=alternative_path
        )
        with open(f"{os.environ['HOME']}/{alternative_path}", "r") as f:
            assert str(f) == test_file_content


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
