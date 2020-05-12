import os
import requests
import logging

from origo.sdk import SDK
from origo.io_utils import write_file_content


log = logging.getLogger()


class DataExporterClient(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "download"
        super().__init__(config, auth, env)
        self.data_exporter_url = self.config.get("dataExporterUrl")

    def get_download_urls(self, dataset_id, version, edition):

        get_download_urls_url = (
            f"{self.data_exporter_url}/{dataset_id}/{version}/{edition}"
        )

        response = self.get(get_download_urls_url)
        return response.json()

    def download_files(self, dataset_id, version, edition, output_path=None):
        download_urls = self.get_download_urls(dataset_id, version, edition)
        downloaded_files = []
        for download_url in download_urls:
            if output_path:
                file_path = f"{os.environ['HOME']}/{output_path}"
            else:
                default_path = "/".join(download_url["key"].split("/")[0:-1])
                file_path = f"{os.environ['HOME']}/{default_path}"

            file_name = download_url["key"].split("/")[-1]
            file_content_response = requests.get(download_url["url"])
            file_content_response.raise_for_status()

            write_file_content(file_name, file_path, file_content_response.text)
            downloaded_files.append(f"{file_path}/{file_name}")

        return {"downloaded_files": downloaded_files}
