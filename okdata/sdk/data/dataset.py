import logging
import re

from okdata.sdk import SDK

log = logging.getLogger()


class Dataset(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "dataset"
        super().__init__(config, auth, env)

    def create_dataset(self, data=None, retries=0):
        url = self.config.get("datasetUrl")
        log.info(f"SDK:Creating dataset with payload: {data}")
        result = self.post(url, data, retries=retries)
        body = result.json()
        log.info(f"Created dataset: {body['Id']}")
        return body

    def get_datasets(self, filter=None, retries=0):
        url = self.config.get("datasetUrl")
        log.info(f"SDK:Get datasets from: {url}")
        result = self.get(url, retries=retries)
        ret = result.json()
        if filter is not None:
            if isinstance(filter, str):
                tmp = []
                for el in ret:
                    if "title" in el and re.match(filter, el["title"], re.IGNORECASE):
                        tmp.append(el)
                ret = tmp
        return ret

    def get_dataset(self, datasetid, retries=0):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}"
        log.info(f"SDK:Getting dataset: {datasetid} from: {url}")
        return self.get(url, retries=retries).json()

    def update_dataset(self, datasetid, data, partial=False, retries=0):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}"
        log.info(f"SDK:Updating dataset: {datasetid} with payload: {data}")
        method = self.patch if partial else self.put
        response = method(url, data, retries=retries)
        body = response.json()
        log.info(f"Updated dataset: {body['Id']}")
        return body

    def create_version(self, datasetid, data, retries=0):
        baseUrl = self.config.get("datasetUrl")
        url = f"{baseUrl}/{datasetid}/versions"
        log.info(
            f"SDK:Creating version for: {datasetid} from: {url}, with payload: {data}"
        )
        result = self.post(url, data, retries=retries)

        body = result.json()
        datasetVersion = body["Id"].split("/")[1]
        log.info(f"SDK:Created dataset version: {datasetVersion}")
        return body

    def get_versions(self, datasetid, retries=0):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions"
        log.info(f"SDK:Getting all dataset version for: {datasetid} from: {url}")
        return self.get(url, retries=retries).json()

    def get_latest_version(self, datasetid, retries=0):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions/latest"
        log.info(f"SDK:Getting latest dataset version for: {datasetid} from: {url}")
        return self.get(url, retries=retries).json()

    def update_version(self, datasetid, versionid, data, retries=0):
        baseUrl = self.config.get("datasetUrl")
        url = f"{baseUrl}/{datasetid}/versions/{versionid}"
        log.info(
            f"SDK:Updating version {versionid} for: {datasetid} from: {url}, with payload: {data}"
        )
        result = self.put(url, data, retries=retries)
        body = result.json()
        datasetVersion = body["Id"].split("/")[1]
        log.info(f"SDK:Updated dataset version: {datasetVersion} on {datasetid}")
        return body

    def create_edition(self, datasetid, versionid, data, retries=0):
        baseUrl = self.config.get("datasetUrl")
        url = f"{baseUrl}/{datasetid}/versions/{versionid}/editions"
        log.info(
            f"SDK:Creating dataset edition for: {datasetid} from: {url} with payload: {data}"
        )
        result = self.post(url, data, retries=retries)
        log.info(f"SDK:API reported back: {result.json()}")
        body = result.json()
        editionid = body["Id"].split("/")[2]
        log.info(f"SDK:Created dataset edition: {editionid} on {datasetid}/{versionid}")
        return body

    def get_editions(self, datasetid, versionid, retries=0):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions/{versionid}/editions"
        log.info(
            f"SDK:Getting version editions for: {datasetid}/{versionid} from: {url}"
        )
        return self.get(url, retries=retries).json()

    def get_edition(self, datasetid, versionid, editionid, retries=0):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions/{versionid}/editions/{editionid}"
        log.info(
            f"SDK:Getting version edition for: {datasetid}/{versionid} from: {url}"
        )
        return self.get(url, retries=retries).json()

    def get_latest_edition(self, datasetid, versionid, retries=0):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions/{versionid}/editions/latest"
        log.info(
            f"SDK:Getting latest dataset version edition for: {datasetid}/{versionid} from: {url}"
        )
        return self.get(url, retries=retries).json()

    def update_edition(self, datasetid, versionid, editionid, data, retries=0):
        baseUrl = self.config.get("datasetUrl")
        url = f"{baseUrl}/{datasetid}/versions/{versionid}/editions/{editionid}"
        log.info(
            f"SDK:Updating dataset edition {editionid} for: {datasetid} from: {url} with payload: {data}"
        )
        result = self.put(url, data, retries=retries)
        body = result.json()
        editionid = body["Id"].split("/")[2]
        log.info(f"SDK:Updated dataset edition: {editionid} on {datasetid}/{versionid}")
        return body

    def get_distributions(self, datasetid, versionid, editionid, retries=0):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions/{versionid}/editions/{editionid}/distributions"
        log.info(
            f"SDK:Getting distributions for: {datasetid}/{versionid}/{editionid} from: {url}"
        )
        return self.get(url, retries=retries).json()

    def get_distribution(
        self, datasetid, versionid, editionid, distributionid, retries=0
    ):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions/{versionid}/editions/{editionid}/distributions/{distributionid}"
        log.info(
            f"SDK:Getting distribution for: {datasetid}/{versionid}/{editionid} from: {url}"
        )
        return self.get(url, retries=retries).json()

    def create_distribution(self, datasetid, versionid, editionid, data, retries=0):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions/{versionid}/editions/{editionid}/distributions"
        log.info(
            f"SDK:Creating dataset distribution for: {datasetid} from: {url} with payload: {data}"
        )
        result = self.post(url, data, retries=retries)
        body = result.json()
        distributionid = body["Id"].split("/")[3]
        log.info(
            f"SDK:Created dataset distribution: {distributionid} on {datasetid}/{versionid}/{editionid}"
        )
        return body

    def update_distribution(
        self, datasetid, versionid, editionid, distributionid, data, retries=0
    ):
        datasetUrl = self.config.get("datasetUrl")
        url = f"{datasetUrl}/{datasetid}/versions/{versionid}/editions/{editionid}/distributions/{distributionid}"
        log.info(
            f"SDK:Updating distribution {distributionid} for: {datasetid} from: {url} with payload: {data}"
        )
        result = self.put(url, data, retries=retries)
        body = result.json()
        distributionid = body["Id"].split("/")[3]
        log.info(
            f"SDK:Updated dataset distribution: {distributionid} on {datasetid}/{versionid}/{editionid}"
        )
        return body
