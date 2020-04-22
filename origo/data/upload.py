import requests
import logging
import os

from origo.sdk import SDK
from origo.exceptions import ApiAuthenticateError


log = logging.getLogger()


class Upload(SDK):
    def __init__(self, config=None, auth=None):
        self.__name__ = "upload"
        super().__init__(config, auth)

    def upload(self, fileName, datasetid, versionid, editionid):
        url = self.config.get("s3BucketUrl")
        log.info(f"Uploading {fileName} to {datasetid} on: {url}")
        if url is None:
            raise KeyError("No s3 Bucket URL set")

        s3SignedData = self.create_s3_signed_data(
            fileName, datasetid, versionid, editionid
        )
        s3Data = {}
        if "message" in s3SignedData:
            # TODO: very specific error raised by the Lambda function, remove later
            raise ApiAuthenticateError(s3SignedData["message"])

        for var in s3SignedData["fields"]:
            s3Data[var] = s3SignedData["fields"][var]

        files = {"file": open(fileName, "rb")}
        result = requests.post(url, data=s3Data, files=files)
        status = s3SignedData.get("status_response", False)
        data = {
            "result": result.status_code == 204,
            "status": status,
        }
        return data

    def create_s3_signed_data(self, fileName, datasetid, versionid, editionid):
        edition = f"{datasetid}/{versionid}/{editionid}"
        data = {"filename": os.path.basename(fileName), "editionId": edition}
        url = self.config.get("uploadUrl")
        log.info(f"Creating s3 signed data with payload: {data} on: {url}")
        if url is None:
            raise KeyError("No Signed S3 URL set")
        return self.post(url, data).json()
