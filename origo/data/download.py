import requests
import logging

from origo.sdk import SDK


log = logging.getLogger()


class Download(SDK):
    def __init__(self, config=None, auth=None):
        self.__name__ = "download"
        super().__init__(config, auth)

    # TODO: the data-exporter repo needs to handle dataset export properly first
    def get_files(self, datasetid, versionid, editionid):
        headers = {
            "Authorization": f"Bearer {self.auth.client_credentials.access_token}"
        }
        url = self.config.get("downloadUrl")
        if url is None:
            raise KeyError("No Signed S3 URL set")

        result = requests.post(url, headers=headers)
        return result.json()
