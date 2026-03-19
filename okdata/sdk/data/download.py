import requests
import logging

from okdata.sdk import SDK
from okdata.sdk.io_utils import write_file_content

log = logging.getLogger()


class DownloadURLAssertionError(Exception):
    def __init__(self, url, expected_prefix):
        super().__init__(
            f"Aborting download because of an unexpected S3 download URL "
            f"(should start with {expected_prefix}): {url}"
        )


class Download(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "download"
        super().__init__(config, auth, env)
        self.data_exporter_url = self.config.get("dataExporterUrl")

    def get_files(self, dataset_id, version, edition, retries=0):
        url = "{}/{}{}/{}/{}".format(
            self.data_exporter_url,
            "" if self.auth.token_provider else "public/",
            dataset_id,
            version,
            edition,
        )
        return self.get(url, retries=retries).json()

    def download(self, dataset_id, version, edition, output_path, retries=0):
        downloaded_files = []
        for file in self.get_files(dataset_id, version, edition, retries=retries):
            file_name = file["key"].split("/")[-1]
            file_url = file["url"]
            base_url = self.config.get("s3DownloadBaseUrl")

            if not file_url.startswith(base_url):
                raise DownloadURLAssertionError(file_url, base_url)

            file_content_response = requests.get(file_url, stream=True)
            file_content_response.raise_for_status()

            write_file_content(file_name, output_path, file_content_response.raw.read())
            downloaded_files.append(f"{output_path}/{file_name}")

        return {"files": downloaded_files}
