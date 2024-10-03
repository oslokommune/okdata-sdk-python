import logging
import re
from datetime import datetime

from okdata.sdk import SDK

log = logging.getLogger()


class Dataset(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "dataset"
        super().__init__(config, auth, env)

    def _mk_url(self, *parts):
        """Return a dataset API URL consisting of `parts`.

        Elements in `parts` are separated by slashes and prefixed by a base
        dataset API URL.
        """
        return "/".join([self.config.get("datasetUrl"), *map(str, filter(None, parts))])

    def create_dataset(self, data=None, retries=0):
        log.info(f"SDK:Creating dataset with payload: {data}")
        result = self.post(self._mk_url(), data, retries=retries)
        body = result.json()
        log.info(f"Created dataset: {body['Id']}")
        return body

    def _matches(self, dataset, pattern):
        """Return true if `dataset`'s ID or name matches `pattern`."""
        return re.search(pattern, dataset["Id"], re.IGNORECASE) or (
            "title" in dataset and re.search(pattern, dataset["title"], re.IGNORECASE)
        )

    def get_datasets(self, filter=None, retries=0):
        url = self._mk_url()
        log.info(f"SDK:Get datasets from: {url}")
        datasets = self.get(url, retries=retries).json()
        if isinstance(filter, str):
            return [d for d in datasets if self._matches(d, filter)]
        return datasets

    def get_dataset(self, dataset_id, retries=0):
        url = self._mk_url(dataset_id)
        log.info(f"SDK:Getting dataset: {dataset_id} from: {url}")
        return self.get(url, retries=retries).json()

    def update_dataset(self, dataset_id, data, partial=False, retries=0):
        url = self._mk_url(dataset_id)
        log.info(f"SDK:Updating dataset: {dataset_id} with payload: {data}")
        method = self.patch if partial else self.put
        response = method(url, data, retries=retries)
        body = response.json()
        log.info(f"Updated dataset: {body['Id']}")
        return body

    def create_version(self, dataset_id, data, retries=0):
        url = self._mk_url(dataset_id, "versions")
        log.info(
            f"SDK:Creating version for: {dataset_id} from: {url}, with payload: {data}"
        )
        result = self.post(url, data, retries=retries)

        body = result.json()
        version = body["Id"].split("/")[1]
        log.info(f"SDK:Created dataset version: {version}")
        return body

    def get_versions(self, dataset_id, retries=0):
        url = self._mk_url(dataset_id, "versions")
        log.info(f"SDK:Getting all dataset version for: {dataset_id} from: {url}")
        return self.get(url, retries=retries).json()

    def get_latest_version(self, dataset_id, retries=0):
        url = self._mk_url(dataset_id, "versions", "latest")
        log.info(f"SDK:Getting latest dataset version for: {dataset_id} from: {url}")
        return self.get(url, retries=retries).json()

    def update_version(self, dataset_id, version, data, retries=0):
        url = self._mk_url(dataset_id, "versions", version)
        log.info(
            f"SDK:Updating version {version} for: {dataset_id} from: {url}, with payload: {data}"
        )
        result = self.put(url, data, retries=retries)
        body = result.json()
        version_ = body["Id"].split("/")[1]
        log.info(f"SDK:Updated dataset version: {version_} on {dataset_id}")
        return body

    def delete_version(self, dataset_id, version, cascade=False, retries=0):
        url = self._mk_url(
            dataset_id, "versions", version, "?cascade=true" if cascade else ""
        )
        log.info(f"SDK:Deleting version {version} for: {dataset_id} from: {url}")
        self.delete(url, retries=retries)
        log.info(f"SDK:Deleted dataset version: {version} on {dataset_id}")

    def create_edition(self, dataset_id, version, data, retries=0):
        url = self._mk_url(dataset_id, "versions", version, "editions")
        log.info(
            f"SDK:Creating dataset edition for: {dataset_id} from: {url} with payload: {data}"
        )
        result = self.post(url, data, retries=retries)
        log.info(f"SDK:API reported back: {result.json()}")
        body = result.json()
        edition = body["Id"].split("/")[2]
        log.info(f"SDK:Created dataset edition: {edition} on {dataset_id}/{version}")
        return body

    def auto_create_edition(self, dataset_id, version):
        """Create an automatically named edition for the given dataset version.

        Return the name of the newly created edition.
        """
        data = {
            "edition": datetime.now().astimezone().replace(microsecond=0).isoformat(),
            "description": f"Auto-created edition for {dataset_id}/{version}",
        }
        log.info(f"Creating new edition for {dataset_id}/{version} with data: {data}")
        edition = self.create_edition(dataset_id, version, data)
        log.info(f"Created edition: {edition}")
        return edition

    def get_editions(self, dataset_id, version, retries=0):
        url = self._mk_url(dataset_id, "versions", version, "editions")
        log.info(
            f"SDK:Getting version editions for: {dataset_id}/{version} from: {url}"
        )
        return self.get(url, retries=retries).json()

    def get_edition(self, dataset_id, version, edition, retries=0):
        url = self._mk_url(dataset_id, "versions", version, "editions", edition)
        log.info(f"SDK:Getting version edition for: {dataset_id}/{version} from: {url}")
        return self.get(url, retries=retries).json()

    def get_latest_edition(self, dataset_id, version, retries=0):
        url = self._mk_url(dataset_id, "versions", version, "editions", "latest")
        log.info(
            f"SDK:Getting latest dataset version edition for: {dataset_id}/{version} from: {url}"
        )
        return self.get(url, retries=retries).json()

    def update_edition(self, dataset_id, version, edition, data, retries=0):
        url = self._mk_url(dataset_id, "versions", version, "editions", edition)
        log.info(
            f"SDK:Updating dataset edition {edition} for: {dataset_id} from: {url} with payload: {data}"
        )
        result = self.put(url, data, retries=retries)
        body = result.json()
        edition_ = body["Id"].split("/")[2]
        log.info(f"SDK:Updated dataset edition: {edition_} on {dataset_id}/{version}")
        return body

    def delete_edition(self, dataset_id, version, edition, cascade=False, retries=0):
        url = self._mk_url(
            dataset_id,
            "versions",
            version,
            "editions",
            edition,
            "?cascade=true" if cascade else "",
        )
        log.info(f"SDK:Deleting edition {edition} for: {dataset_id} from: {url}")
        self.delete(url, retries=retries)
        log.info(f"SDK:Deleted dataset edition: {edition} on {dataset_id}/{version}")

    def get_distributions(self, dataset_id, version, edition, retries=0):
        url = self._mk_url(
            dataset_id, "versions", version, "editions", edition, "distributions"
        )
        log.info(
            f"SDK:Getting distributions for: {dataset_id}/{version}/{edition} from: {url}"
        )
        return self.get(url, retries=retries).json()

    def get_distribution(self, dataset_id, version, edition, dist, retries=0):
        url = self._mk_url(
            dataset_id, "versions", version, "editions", edition, "distributions", dist
        )
        log.info(
            f"SDK:Getting distribution for: {dataset_id}/{version}/{edition} from: {url}"
        )
        return self.get(url, retries=retries).json()

    def create_distribution(self, dataset_id, version, edition, data, retries=0):
        url = self._mk_url(
            dataset_id, "versions", version, "editions", edition, "distributions"
        )
        log.info(
            f"SDK:Creating dataset distribution for: {dataset_id} from: {url} with payload: {data}"
        )
        result = self.post(url, data, retries=retries)
        body = result.json()
        dist = body["Id"].split("/")[3]
        log.info(
            f"SDK:Created dataset distribution: {dist} on {dataset_id}/{version}/{edition}"
        )
        return body

    def update_distribution(self, dataset_id, version, edition, dist, data, retries=0):
        url = self._mk_url(
            dataset_id, "versions", version, "editions", edition, "distributions", dist
        )
        log.info(
            f"SDK:Updating distribution {dist} for: {dataset_id} from: {url} with payload: {data}"
        )
        result = self.put(url, data, retries=retries)
        body = result.json()
        dist_ = body["Id"].split("/")[3]
        log.info(
            f"SDK:Updated dataset distribution: {dist_} on {dataset_id}/{version}/{edition}"
        )
        return body

    def delete_distribution(self, dataset_id, version, edition, dist, retries=0):
        url = self._mk_url(
            dataset_id, "versions", version, "editions", edition, "distributions", dist
        )
        log.info(f"SDK:Deleting distribution {dist} for: {dataset_id} from: {url}")
        self.delete(url, retries=retries)
        log.info(
            f"SDK:Deleted dataset distribution: {dist} on {dataset_id}/{version}/{edition}"
        )
