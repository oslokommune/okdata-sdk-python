import logging
import re

from origo.sdk import SDK
from origo.exceptions import DataExistsError

log = logging.getLogger()


class Dataset(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "dataset"
        super().__init__(config, auth, env)

    def create_dataset(self, data=None):
        url = self.config.get("datasetUrl")
        log.info(f"SDK:Creating dataset with data: {data}")
        result = self.post(url, data)
        body = result.json()
        log.info(f"Created dataset: {body['Id']}")
        return body

    def get_datasets(self, filter=None):
        url = self.config.get("datasetUrl")
        log.info(f"SDK:Get datasets from: {url}")
        result = self.get(url)
        ret = result.json()
        if filter is not None:
            if isinstance(filter, str):
                tmp = []
                for el in ret:
                    if "title" in el and re.match(filter, el["title"], re.IGNORECASE):
                        tmp.append(el)
                ret = tmp
        return ret

    def get_dataset(self, datasetid):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}"
        log.info(f"SDK:Getting dataset: {datasetid} from: {url}")
        return self.get(url).json()

    def create_version(self, datasetid, data):
        baseUrl = self.config.get("datasetUrl")
        url = f"{baseUrl}/{datasetid}/versions"
        log.info(
            f"SDK:Creating version for {datasetid} from: {url}, with payload: {data}"
        )
        result = self.post(url, data)
        if result.status_code == 409:
            version = data["version"]
            raise DataExistsError(
                f"Version: {version} on datasetId {datasetid} already exists"
            )
        body = result.json()
        datasetVersion = body["Id"].split("/")[1]
        log.info(f"SDK:Created dataset version: {datasetVersion}")
        return body

    def get_versions(self, datasetid):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions"
        log.info(f"SDK:Getting all dataset version for: {datasetid} from: {url}")
        return self.get(url).json()

    def get_latest_version(self, datasetid):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions/latest"
        log.info(f"SDK:Getting latest dataset version for: {datasetid} from: {url}")
        return self.get(url).json()

    def create_edition(self, datasetid, versionid, data):
        baseUrl = self.config.get("datasetUrl")
        url = f"{baseUrl}/{datasetid}/versions/{versionid}/editions"
        log.info(
            f"SDK:Creating dataset edition for: {datasetid} from: {url} with payload: {data}"
        )
        result = self.post(url, data)
        log.info(f"SDK:API reported back: {result.json()}")
        if result.status_code == 409:
            edition = data["edition"]
            raise DataExistsError(
                f"Edition: {edition} on datasetId {datasetid} version: {versionid} already exists"
            )
        body = result.json()
        editionid = body["Id"].split("/")[2]
        log.info(f"SDK:Created dataset edition: {editionid} on {datasetid}/{versionid}")
        return body

    def get_editions(self, datasetid, versionid):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions/{versionid}/editions"
        log.info(
            f"SDK:Getting version editions for: {datasetid}/{versionid} from: {url}"
        )
        return self.get(url).json()

    def get_edition(self, datasetid, versionid, editionid):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions/{versionid}/editions/{editionid}"
        log.info(
            f"SDK:Getting version edition for: {datasetid}/{versionid} from: {url}"
        )
        return self.get(url).json()

    def get_latest_edition(self, datasetid, versionid):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions/{versionid}/editions/latest"
        log.info(
            f"SDK:Getting latest dataset version edition for {datasetid}/{versionid} from: {url}"
        )
        return self.get(url).json()

    def get_distributions(self, datasetid, versionid, editionid):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions/{versionid}/editions/{editionid}/distributions"
        return self.get(url).json()

    def create_distribution(self, datasetid, versionid, editionid, data):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions/{versionid}/editions/{editionid}/distributions"
        log.info(
            f"SDK:Creating dataset distribution for: {datasetid} from: {url} with payload: {data}"
        )
        result = self.post(url, data)
        body = result.json()
        distributionid = body["Id"].split("/")[3]
        log.info(
            f"SDK:Created dataset distribution: {distributionid} on {datasetid}/{versionid}/{editionid}"
        )
        return body
