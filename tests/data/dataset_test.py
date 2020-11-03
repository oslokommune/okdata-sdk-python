import json
import re
from requests.exceptions import HTTPError

from origo.sdk.data.dataset import Dataset
from origo.sdk.auth.auth import Authenticate
from origo.sdk.config import Config
from origo.sdk.file_cache import FileCache

config = Config()
file_cache = FileCache(config)
file_cache.credentials_cache_enabled = False
auth_default = Authenticate(config, file_cache=file_cache)


class TestDataset:
    def test_createDataset(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset-createDataset"})
        matcher = re.compile("datasets")
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)
        body = ds.create_dataset({"Id": "test-dataset-createDataset"})
        assert body["Id"] == "test-dataset-createDataset"

    def test_sdk_no_auth_headers(self):
        del config.config["client_id"]
        del config.config["client_secret"]
        ds = Dataset(config=config)

        assert ds.headers() == {}

    def test_getDatasets(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps([{"Id": "test-get-dataset"}])
        matcher = re.compile("datasets")
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        list = ds.get_datasets()
        assert list[0]["Id"] == "test-get-dataset"

    def test_getDatasets_filter_no_result(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps(
            [{"Id": "foo-bar", "title": "deichman", "publisher": "someone"}]
        )
        matcher = re.compile("datasets")
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        list = ds.get_datasets("eide")
        assert len(list) == 0

    def test_getDatasets_filter(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps(
            [{"Id": "foo-bar", "title": "eide"}, {"Id": "foo-bar2", "title": "someone"}]
        )
        matcher = re.compile("datasets")
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        list = ds.get_datasets("eide")
        assert len(list) == 1

    def test_getDataset(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-get-dataset"})
        matcher = re.compile("datasets/test-get-dataset")
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        dataset = ds.get_dataset("test-get-dataset")
        assert dataset["Id"] == "test-get-dataset"


class TestVersion:
    def test_createDatasetVersion(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset-createdataset-version/1"})
        matcher = re.compile("datasets/test-dataset-createdataset-version/versions")
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)
        version = ds.create_version("test-dataset-createdataset-version", {})
        assert version["Id"] == "test-dataset-createdataset-version/1"

    def test_createDatasetVersion_exists(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps("test-dataset-createdataset-exists/1")
        matcher = re.compile("datasets/test-dataset-createdataset-exists/versions")
        requests_mock.register_uri("POST", matcher, text=response, status_code=409)
        try:
            ds.create_version("test-dataset-createdataset-exists", {"version": "1"})
            assert False
        except HTTPError as e:
            assert e.response.status_code == 409
            assert True

    def test_getDatasetVersions(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps([{"Id": "test-dataset-versions"}])
        matcher = re.compile("datasets/test-dataset-versions/versions")
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        list = ds.get_versions("test-dataset-versions")
        assert len(list) == 1

    def test_getDatasetVersionsLatest(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset-version-latest"})
        matcher = re.compile("datasets/test-dataset-version-latest/versions/latest")
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        version = ds.get_latest_version("test-dataset-version-latest")
        assert version["Id"] == "test-dataset-version-latest"


class TestEdition:
    def test_createDatasetVersionEdition(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps(
            {"Id": "test-dataset-createdataset-edition/1/test-edition"}
        )
        matcher = re.compile(
            "datasets/test-dataset-createdataset-edition/versions/1/editions"
        )
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)
        edition = ds.create_edition("test-dataset-createdataset-edition", 1, {})
        assert edition["Id"] == "test-dataset-createdataset-edition/1/test-edition"

    def test_getDatasetVersionEditions(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps([{"Id": "test-dataset-get-dataset-version-editions"}])
        matcher = re.compile(
            "datasets/test-dataset-get-dataset-version-editions/versions/1/editions"
        )
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        list = ds.get_editions("test-dataset-get-dataset-version-editions", 1)
        assert len(list) == 1

    def test_getDatasetVersionEdition(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset-version-edition"})
        matcher = re.compile(
            "datasets/test-dataset-version-edition/versions/1/editions/my-edition"
        )
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        edition = ds.get_edition("test-dataset-version-edition", 1, "my-edition")
        assert edition["Id"] == "test-dataset-version-edition"

    def test_getDatasetVersionEditionLatest(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset-edition-latest"})
        matcher = re.compile(
            "datasets/test-dataset-edition-latest/versions/1/editions/latest"
        )
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        edition = ds.get_latest_edition("test-dataset-edition-latest", 1)
        assert edition["Id"] == "test-dataset-edition-latest"
