import json
import re
from unittest.mock import patch, mock_open

from origo.sdk.data.upload import Upload
from origo.sdk.auth.auth import Authenticate
from origo.sdk.config import Config
from origo.sdk.file_cache import FileCache
from tests.auth.client_credentials_test_utils import (
    default_test_client_credentials,
)


config = Config()
file_cache = FileCache(config)
file_cache.credentials_cache_enabled = False
auth_default = Authenticate(config, file_cache=file_cache)

auth_default.client_credentials = default_test_client_credentials


data_uploader_response = {
    "url": "https://aws/bucket",
    "fields": {"a": "b"},
    "trace_id": "uu-ii-dd",
}


class TestUpload:
    def test_upload(self, requests_mock):
        up = Upload(config=config, auth=auth_default)
        response = json.dumps(data_uploader_response)
        matcher = re.compile(config.get("uploadUrl"))
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)

        s3Response = json.dumps({"url": "https://aws/bucket", "fields": {"a": "b"}})
        s3matcher = re.compile(config.get("s3BucketUrl"))
        requests_mock.register_uri("POST", s3matcher, text=s3Response, status_code=204)

        with patch("builtins.open", mock_open(read_data="file-name")):
            res = up.upload("file-name", "dataset-id", "version-id", "edition-id")
            assert res["result"] is True
            assert res["trace_id"] == "uu-ii-dd"

    def test_createS3SignedData(self, requests_mock):
        up = Upload(config=config, auth=auth_default)
        response = json.dumps(data_uploader_response)
        matcher = re.compile(config.get("uploadUrl"))
        requests_mock.register_uri("POST", matcher, text=response, status_code=200)
        data = up.create_s3_signed_data(
            "file.txt", "my-dataset", "my-versionid", "my-editionid"
        )
        assert data["trace_id"] == "uu-ii-dd"
