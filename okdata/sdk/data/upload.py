import logging
import os

from okdata.sdk import SDK
from okdata.sdk.exceptions import ApiAuthenticateError


log = logging.getLogger()


class Upload(SDK):
    def __init__(self, config=None, auth=None):
        self.__name__ = "upload"
        super().__init__(config, auth)

    def upload(self, fileName, datasetid, versionid, editionid, retries=0):
        url = self.config.get("s3BucketUrl")
        log.info(f"Uploading {fileName} to {datasetid} on: {url}")
        if url is None:
            raise KeyError("No s3 Bucket URL set")

        s3SignedData = self.create_s3_signed_data(
            fileName, datasetid, versionid, editionid, retries=retries
        )
        s3Data = {}
        if "message" in s3SignedData:
            # TODO: very specific error raised by the Lambda function, remove later
            raise ApiAuthenticateError(s3SignedData["message"])

        for var in s3SignedData["fields"]:
            s3Data[var] = s3SignedData["fields"][var]

        with open(fileName, "rb") as file:
            files = {"file": file}
            upload_session = self.prepared_request_with_retries(retries=retries)
            result = upload_session.post(url, data=s3Data, files=files)
            trace_id = s3SignedData.get("trace_id")
            data = {"result": result.status_code == 204, "trace_id": trace_id}
            return data

    def create_s3_signed_data(
        self, fileName, datasetid, versionid, editionid, retries=0
    ):
        edition = f"{datasetid}/{versionid}/{editionid}"
        data = {"filename": os.path.basename(fileName), "editionId": edition}
        url = self.config.get("uploadUrl")
        log.info(f"Creating s3 signed data with payload: {data} on: {url}")
        if url is None:
            raise KeyError("No Signed S3 URL set")
        return self.post(url, data, retries=retries).json()
