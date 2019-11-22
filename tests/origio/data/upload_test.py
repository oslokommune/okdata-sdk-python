import json
import re
from unittest.mock import patch, mock_open

from origo.data.upload import Upload
from origo.auth.auth import Authenticate
from origo.config import Config
from origo.file_cache import FileCache
from tests.origio.auth.client_credentials_test_utils import (
    default_test_client_credentials,
)


config = Config()
file_cache = FileCache(config)
file_cache.credentials_cache_enabled = False
auth_default = Authenticate(config, file_cache=file_cache)

auth_default.client_credentials = default_test_client_credentials


class TestUpload:
    def test_upload(self, requests_mock):
        up = Upload(config=config, auth=auth_default)
        response = json.dumps(
            {
                "Id": "test-upload-create-signed-data",
                "fields": {"a": "b"},
                "status_code": 204,
            }
        )
        matcher = re.compile(config.get("uploadUrl"))
        requests_mock.register_uri("POST", matcher, text=response, status_code=204)

        s3Response = json.dumps({"status_code": 204, "fields": {"a": "b"}})
        s3matcher = re.compile(config.get("s3BucketUrl"))
        requests_mock.register_uri("POST", s3matcher, text=s3Response, status_code=204)

        with patch("builtins.open", mock_open(read_data="file-name")):
            res = up.upload("file-name", "dataset-id", "version-id", "edition-id")
            assert res is True

    def test_createS3SignedData(self, requests_mock):
        up = Upload(config=config, auth=auth_default)
        response = json.dumps({"Id": "test-upload-create-signed-data"})
        matcher = re.compile(config.get("uploadUrl"))
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)
        data = up.create_s3_signed_data(
            "file.txt", "my-dataset", "my-versionid", "my-editionid"
        )
        assert data["Id"] == "test-upload-create-signed-data"
