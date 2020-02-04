import logging

from origo.sdk import SDK

log = logging.getLogger(__name__)


class InternalError(Exception):
    pass


class NotDatasetOwnerError(Exception):
    pass


class ElasticsearchQueries(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "elasticsearch_queries"
        super().__init__(config, auth, env)
        self.elasticsearch_query_url = self.config.get("elasticsearchQueryUrl")

    def event_stat(self, dataset_id):
        url = f"{self.elasticsearch_query_url}/{dataset_id}/events"
        res = self.get(url)
        log.debug(f"event stat status: {res.status_code}")

        if res.status_code == 403:
            log.debug(f"event stat message: {res.text}")
            raise NotDatasetOwnerError

        if res.status_code != 200:
            log.error(f"event stat message: {res.text}")
            raise InternalError

        return res.json()
