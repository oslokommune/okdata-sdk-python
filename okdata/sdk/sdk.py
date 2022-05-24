import logging
import requests
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

    def _request(self, method, url, retries, **kwargs):
        session = self.prepared_request_with_retries(retries)
        try:
            request_method = getattr(session, method)
        except AttributeError:
            raise ValueError(f"'{method}' is not a valid request method")
        log.info(f"SDK:Making a {method.upper()} request to URL: {url}")
        response = request_method(url, headers=self.headers(), **kwargs)
        response.raise_for_status()
        return response

    def post(self, url, data, retries=0, **kwargs):
        return self._request("post", url, retries, json=data, **kwargs)

    def put(self, url, data, retries=0, **kwargs):
        return self._request("put", url, retries, json=data, **kwargs)

    def patch(self, url, data, retries=0, **kwargs):
        return self._request("patch", url, retries, json=data, **kwargs)

    def get(self, url, retries=0, **kwargs):
        return self._request("get", url, retries, **kwargs)

    def delete(self, url, retries=0, **kwargs):
        return self._request("delete", url, retries, **kwargs)

    @staticmethod
    def prepared_request_with_retries(retries):
        #  https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure
        retry_strategy = Retry(
            status=retries,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1,
            allowed_methods=[
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
