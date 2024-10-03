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
    def test_mk_url(self):
        ds = Dataset(config=config)
        base_url = config.get("datasetUrl")
        assert ds._mk_url() == base_url
        assert ds._mk_url("datasets") == f"{base_url}/datasets"
        assert ds._mk_url("datasets", "x") == f"{base_url}/datasets/x"
        assert ds._mk_url("datasets", "x", "") == f"{base_url}/datasets/x"

    def test_create_dataset(self, requests_mock):
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

    def test_get_dataset(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-get-dataset"})
        matcher = re.compile("datasets/test-get-dataset")
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        dataset = ds.get_dataset("test-get-dataset")
        assert dataset["Id"] == "test-get-dataset"

    def test_update_dataset(self, requests_mock):
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
    def test_create_version(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset-createdataset-version/1"})
        matcher = re.compile("datasets/test-dataset-createdataset-version/versions")
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)
        version = ds.create_version("test-dataset-createdataset-version", {})
        assert version["Id"] == "test-dataset-createdataset-version/1"

    def test_create_version_exists(self, requests_mock):
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

    def test_get_versions(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps([{"Id": "test-dataset-versions"}])
        matcher = re.compile("datasets/test-dataset-versions/versions")
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        versions = ds.get_versions("test-dataset-versions")
        assert len(versions) == 1

    def test_get_latest_version(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset-version-latest"})
        matcher = re.compile("datasets/test-dataset-version-latest/versions/latest")
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        version = ds.get_latest_version("test-dataset-version-latest")
        assert version["Id"] == "test-dataset-version-latest"

    def test_update_version(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset-update-version/1"})
        matcher = re.compile("datasets/test-dataset-update-version/versions")
        requests_mock.register_uri("PUT", matcher, text=response, status_code=200)
        version = ds.update_version("test-dataset-update-version", 1, {"some": "data"})
        assert requests_mock.last_request.json() == {"some": "data"}
        assert version["Id"] == "test-dataset-update-version/1"

    def test_update_version_invalid(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset-update-version/1"})
        matcher = re.compile("datasets/test-dataset-update-version/versions")
        requests_mock.register_uri("PUT", matcher, text=response, status_code=409)
        with pytest.raises(HTTPError):
            ds.update_version("test-dataset-update-version", 1, {"version": "2"})

    def test_delete_version(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        matcher = re.compile("datasets/foo/versions/1")
        requests_mock.register_uri("DELETE", matcher, status_code=200)
        ds.delete_version("foo", "1")
        assert (
            requests_mock.last_request.url
            == f"{config.get('datasetUrl')}/foo/versions/1"
        )
        assert requests_mock.last_request.method == "DELETE"


class TestEdition:
    def test_create_edition(self, requests_mock):
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

    def test_auto_create_edition(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset/1/test-edition"})
        matcher = re.compile("datasets/test-dataset/versions/1/editions")
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)
        assert (
            ds.auto_create_edition("test-dataset", "1")["Id"]
            == "test-dataset/1/test-edition"
        )

    def test_get_editions(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps([{"Id": "test-dataset-get-dataset-version-editions"}])
        matcher = re.compile(
            "datasets/test-dataset-get-dataset-version-editions/versions/1/editions"
        )
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        list = ds.get_editions("test-dataset-get-dataset-version-editions", 1)
        assert len(list) == 1

    def test_get_edition(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset-version-edition"})
        matcher = re.compile(
            "datasets/test-dataset-version-edition/versions/1/editions/my-edition"
        )
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        edition = ds.get_edition("test-dataset-version-edition", 1, "my-edition")
        assert edition["Id"] == "test-dataset-version-edition"

    def test_get_latest_edition(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-dataset-edition-latest"})
        matcher = re.compile(
            "datasets/test-dataset-edition-latest/versions/1/editions/latest"
        )
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        edition = ds.get_latest_edition("test-dataset-edition-latest", 1)
        assert edition["Id"] == "test-dataset-edition-latest"

    def test_update_edition(self, requests_mock):
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

    def test_delete_edition(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        matcher = re.compile("datasets/foo/versions/1/editions/bar")
        requests_mock.register_uri("DELETE", matcher, status_code=200)
        ds.delete_edition("foo", "1", "bar")
        assert (
            requests_mock.last_request.url
            == f"{config.get('datasetUrl')}/foo/versions/1/editions/bar"
        )
        assert requests_mock.last_request.method == "DELETE"


class TestDistribution:
    def test_create_distribution(self, requests_mock):
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

    def test_get_distributions(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps([{"Id": "my-dataset"}])
        matcher = re.compile(
            "datasets/my-dataset/versions/1/editions/my-edition/distributions"
        )
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        distributions = ds.get_distributions("my-dataset", 1, "my-edition")
        assert len(distributions) == 1

    def test_get_distribution(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        response = json.dumps({"Id": "my-dataset/1/my-edition/my-distro"})
        matcher = re.compile(
            "datasets/my-dataset/versions/1/editions/my-edition/distributions/my-distro"
        )
        requests_mock.register_uri("GET", matcher, text=response, status_code=200)
        distribution = ds.get_distribution("my-dataset", 1, "my-edition", "my-distro")
        assert distribution["Id"] == "my-dataset/1/my-edition/my-distro"

    def test_update_distribution(self, requests_mock):
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

    def test_delete_distribution(self, requests_mock):
        ds = Dataset(config=config, auth=auth_default)
        matcher = re.compile("datasets/foo/versions/1/editions/bar/distributions/baz")
        requests_mock.register_uri("DELETE", matcher, status_code=200)
        ds.delete_distribution("foo", "1", "bar", "baz")
        assert (
            requests_mock.last_request.url
            == f"{config.get('datasetUrl')}/foo/versions/1/editions/bar/distributions/baz"
        )
        assert requests_mock.last_request.method == "DELETE"
