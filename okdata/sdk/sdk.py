import logging
import requests
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from okdata.sdk.config import Config
from okdata.sdk.auth.auth import Authenticate

log = logging.getLogger()


class SDK(object):
    def __init__(self, config=None, auth=None, env=None):
        self.config = config
        if self.config is None:
            log.info("Initializing configuration object")
            self.config = Config(env=env)
        self.auth = auth
        if self.auth is None:
            log.info("Initializing auth object")
            self.auth = Authenticate(self.config)

    def login(self):
        self.auth.login()

    def headers(self):
        headers = {}
        if self.auth.token_provider:
            headers["Authorization"] = f"Bearer {self.auth.access_token}"
        return headers

    def post(self, url, data, retries=0, **kwargs):
        log.info(f"SDK:Posting resource to url: {url}")
        session = self.prepared_request_with_retries(retries)
        result = session.post(
            url, data=json.dumps(data), headers=self.headers(), **kwargs
        )
        result.raise_for_status()
        return result

    def put(self, url, data, retries=0, **kwargs):
        log.info(f"SDK:Putting resource to url: {url}")
        session = self.prepared_request_with_retries(retries)
        result = session.put(
            url, data=json.dumps(data), headers=self.headers(), **kwargs
        )
        result.raise_for_status()
        return result

    def get(self, url, retries=0, **kwargs):
        log.info(f"SDK:Getting resource from url: {url}")
        session = self.prepared_request_with_retries(retries)
        result = session.get(url, headers=self.headers(), **kwargs)
        result.raise_for_status()
        return result

    def delete(self, url, retries=0, **kwargs):
        log.info(f"SDK:Deleting resource from url: {url}")
        session = self.prepared_request_with_retries(retries)
        result = session.delete(url, headers=self.headers(), **kwargs)
        result.raise_for_status()
        return result

    @staticmethod
    def prepared_request_with_retries(retries):
        #  https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure
        retry_strategy = Retry(
            total=retries,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1,
            method_whitelist=[
                "HEAD",
                "GET",
                "PUT",
                "POST",
                "DELETE",
                "OPTIONS",
                "TRACE",
            ],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        return session
