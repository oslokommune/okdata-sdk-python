import requests
import logging
import os

from origo.sdk import SDK
from origo.exceptions import ApiAuthenticateError


log = logging.getLogger()


class Status(SDK):
    def __init__(self, config=None, auth=None):
        self.__name__ = "status"
        super().__init__(config, auth)

    def get_status(self):
        return "status"
