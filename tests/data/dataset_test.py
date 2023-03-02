import json
import re

import pytest
from requests.exceptions import HTTPError

from okdata.sdk.auth.auth import Authenticate
from okdata.sdk.config import Config
from okdata.sdk.data.dataset import Dataset
from okdata.sdk.file_cache import FileCache

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

    def test_get_datasets(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps([{"Id": "test-get-datasets"}])
        matcher = re.compile("datasets")
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        res = ds.get_datasets()
        assert [d["Id"] for d in res] == ["test-get-datasets"]

    def test_get_datasets_filter_no_results(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps(
            [{"Id": "foo-bar", "title": "deichman", "publisher": "someone"}]
        )
        matcher = re.compile("datasets")
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        assert ds.get_datasets("eide") == []

    def test_get_datasets_filter_by_id(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps(
            [{"Id": "foo-bar", "title": "eide"}, {"Id": "foo-bar2", "title": "someone"}]
        )
        matcher = re.compile("datasets")
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        res = ds.get_datasets("bar2")
        assert [d["Id"] for d in res] == ["foo-bar2"]

    def test_get_datasets_filter_by_title(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps(
            [{"Id": "foo-bar", "title": "eide"}, {"Id": "foo-bar2", "title": "someone"}]
        )
        matcher = re.compile("datasets")
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        res = ds.get_datasets("eide")
        assert [d["Id"] for d in res] == ["foo-bar"]

    def test_getDataset(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-get-dataset"})
        matcher = re.compile("datasets/test-get-dataset")
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        dataset = ds.get_dataset("test-get-dataset")
        assert dataset["Id"] == "test-get-dataset"

    def test_updateDataset(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        datasetid = "test-dataset-updateDataset"
        matcher = re.compile(f"datasets/{datasetid}")
        response = json.dumps({"Id": datasetid})
        requests_mock.register_uri("PUT", matcher, text=response, status_code=200)
        body = ds.update_dataset(datasetid, {"Id": datasetid})
        assert body["Id"] == datasetid

    def test_update_dataset_partial(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        dataset_id = "test-dataset-update-partial"
        matcher = re.compile(f"datasets/{dataset_id}")
        response = json.dumps({"Id": dataset_id})
        requests_mock.register_uri("PATCH", matcher, text=response, status_code=200)
        body = ds.update_dataset(dataset_id, {"Id": dataset_id}, partial=True)
        assert body["Id"] == dataset_id


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

    def test_updateDatasetVersion(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset-update-version/1"})
        matcher = re.compile("datasets/test-dataset-update-version/versions")
        requests_mock.register_uri("PUT", matcher, text=response, status_code=200)
        version = ds.update_version("test-dataset-update-version", 1, {"some": "data"})
        assert requests_mock.last_request.json() == {"some": "data"}
        assert version["Id"] == "test-dataset-update-version/1"

    def test_updateDatasetInvalidVersion(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset-update-version/1"})
        matcher = re.compile("datasets/test-dataset-update-version/versions")
        requests_mock.register_uri("PUT", matcher, text=response, status_code=409)
        with pytest.raises(HTTPError):
            ds.update_version("test-dataset-update-version", 1, {"version": "2"})


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

    def test_updateDatasetVersionEdition(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset-updatedataset-edition/1/my-edition"})
        matcher = re.compile(
            "datasets/test-dataset-updatedataset-edition/versions/1/editions/my-edition"
        )
        requests_mock.register_uri("PUT", matcher, text=response, status_code=200)
        edition = ds.update_edition(
            "test-dataset-updatedataset-edition", 1, "my-edition", {"some": "data"}
        )
        assert requests_mock.last_request.json() == {"some": "data"}
        assert edition["Id"] == "test-dataset-updatedataset-edition/1/my-edition"


class TestDistribution:
    def test_createDatasetVersionEditionDistribution(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "my-dataset/1/my-edition/test-distro"})
        matcher = re.compile(
            "datasets/my-dataset/versions/1/editions/my-edition/distributions"
        )
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)
        distribution = ds.create_distribution(
            "my-dataset", 1, "my-edition", {"some": "data"}
        )
        assert requests_mock.last_request.json() == {"some": "data"}
        assert distribution["Id"] == "my-dataset/1/my-edition/test-distro"

    def test_getDatasetVersionEditionDistributions(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps([{"Id": "my-dataset"}])
        matcher = re.compile(
            "datasets/my-dataset/versions/1/editions/my-edition/distributions"
        )
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        list = ds.get_distributions("my-dataset", 1, "my-edition")
        assert len(list) == 1

    def test_getDatasetVersionEditionDistribution(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "my-dataset/1/my-edition/my-distro"})
        matcher = re.compile(
            "datasets/my-dataset/versions/1/editions/my-edition/distributions/my-distro"
        )
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        distribution = ds.get_distribution("my-dataset", 1, "my-edition", "my-distro")
        assert distribution["Id"] == "my-dataset/1/my-edition/my-distro"

    def test_updateDatasetVersionEditionDistribution(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "my-dataset/1/my-edition/my-distro"})
        matcher = re.compile(
            "datasets/my-dataset/versions/1/editions/my-edition/distributions/my-distro"
        )
        requests_mock.register_uri("PUT", matcher, text=response, status_code=200)
        distribution = ds.update_distribution(
            "my-dataset", 1, "my-edition", "my-distro", {"some": "data"}
        )
        assert requests_mock.last_request.json() == {"some": "data"}
        assert distribution["Id"] == "my-dataset/1/my-edition/my-distro"
