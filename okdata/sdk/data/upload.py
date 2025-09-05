import logging
import os

from okdata.sdk import SDK
from okdata.sdk.exceptions import ApiAuthenticateError

log = logging.getLogger()


class Upload(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "upload"
        super().__init__(config, auth, env)

    def upload(self, filename, dataset_id, version, edition, retries=0):
        url = self.config.get("s3BucketUrl")
        log.info(f"Uploading {filename} to {dataset_id} on: {url}")
        if url is None:
            raise KeyError("No S3 bucket URL set")

        s3_signed_data = self.create_s3_signed_data(
            filename, dataset_id, version, edition, retries=retries
        )
        s3_data = {}
        if "message" in s3_signed_data:
            # TODO: Very specific error raised by the Lambda function, remove later
            raise ApiAuthenticateError(s3_signed_data["message"])

        for var in s3_signed_data["fields"]:
            s3_data[var] = s3_signed_data["fields"][var]

        with open(filename, "rb") as file:
            files = {"file": file}
            upload_session = self.prepared_request_with_retries(retries=retries)
            result = upload_session.post(url, data=s3_data, files=files)
            trace_id = s3_signed_data.get("trace_id")
            return {"result": result.status_code == 204, "trace_id": trace_id}

    def create_s3_signed_data(self, filename, dataset_id, version, edition, retries=0):
        edition_id = f"{dataset_id}/{version}/{edition}"
        data = {"filename": os.path.basename(filename), "editionId": edition_id}
        url = self.config.get("uploadUrl")
        log.info(f"Creating S3 signed data with payload: {data} on: {url}")
        if url is None:
            raise KeyError("No signed S3 URL set")
        return self.post(url, data, retries=retries).json()
