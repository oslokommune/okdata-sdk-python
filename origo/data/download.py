import os
import requests
import logging

from origo.sdk import SDK
from origo.io_utils import write_file_content


log = logging.getLogger()


class Download(SDK):
    def __init__(self, config=None, auth=None):
        self.__name__ = "download"
        super().__init__(config, auth)

    # TODO: the data-exporter repo needs to handle dataset export properly first
    def get_download_urls(self, dataset_id, version, edition):
        base_url = self.config.get("downloadUrl")

        get_download_urls_url = f"{base_url}/{dataset_id}/{version}/{edition}"

        result = self.get(get_download_urls_url)
        return result.json()

    def download_files(self, dataset_id, version, edition, output_path=None):
        download_urls = self.get_download_urls(dataset_id, version, edition)
        for download_url in download_urls:
            if output_path:
                file_path = f"{os.environ['HOME']}/{output_path}"
            else:
                default_path = "/".join(download_url['key'].split("/")[0:-1])
                file_path = f"{os.environ['HOME']}/{default_path}"

            file_name = download_url["key"].split("/")[-1]
            file_content = requests.get(download_url["url"]).text

            write_file_content(file_name, file_path, file_content)
