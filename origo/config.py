import os
import logging

from origo.exceptions import ConfigurationError

log = logging.getLogger()

# TODO: Move these to a config file later on
# TODO: use only a single base URL and derive the URLs based on that
ORIGO_CONFIG = {}
ORIGO_CONFIG["dev"] = {
    "client_id": None,
    "client_secret": None,
    "cacheCredentials": False,
    "datasetUrl": "https://api.data-dev.oslo.systems/metadata/datasets",
    "downloadUrl": "https://api.data-dev.oslo.systems/data-exporter",
    "eventCollectorUrl": "https://api.data-dev.oslo.systems/event-collector",
    "keycloakRealm": "api-catalog",
    "keycloakServerUrl": "https://login-test.oslo.kommune.no/auth",
    "pipelineUrl": "https://api.data-dev.oslo.systems/pipeline",
    "s3BucketUrl": "https://s3.eu-west-1.amazonaws.com/ok-origo-dataplatform-dev",
    "streamManagerUrl": "https://api.data-dev.oslo.systems/stream-manager",
    "tokenService": "https://api.data-dev.oslo.systems/token-service/token",
    "uploadUrl": "https://api.data-dev.oslo.systems/data-uploader",
}
ORIGO_CONFIG["prod"] = {
    "client_id": None,
    "client_secret": None,
    "cacheCredentials": True,
    "datasetUrl": "https://api.data.oslo.systems/metadata/datasets",
    "downloadUrl": "https://api.data.oslo.systems/data-exporter",
    "eventCollectorUrl": "https://api.data.oslo.systems/event-collector",
    "keycloakRealm": "api-catalog",
    "keycloakServerUrl": "https://login.oslo.kommune.no/auth",
    "pipelineUrl": "https://api.data.oslo.systems/pipeline",
    "s3BucketUrl": "https://s3.eu-west-1.amazonaws.com/ok-origo-dataplatform-prod",
    "streamManagerUrl": "https://api.data.oslo.systems/stream-manager",
    "tokenService": "https://api.data.oslo.systems/token-service/token",
    "uploadUrl": "https://api.data.oslo.systems/data-uploader",
}

ORIGO_DEFAULT_ENVIRONMENT = "dev"

ORIGO_ENVIRONMENTS = ["dev", "prod"]


class Config:
    def __init__(self, type=None, env=None, config=None):
        if config:
            self.config = config
        else:
            env = self.resolve_environment(env)
            log.info(f"SDK:Using environment: {env}")
            if type is not None:
                self.config = self.create_config_type(type, env)
            else:
                self.config = self.create_config(env)
            if self.config is False:
                raise ConfigurationError(
                    "No configuration found... I have tried everything!"
                )
            self.config["env"] = env

    def resolve_environment(self, env):
        # only load from environment if nothing is passed to constructor
        # parameter > environment > default
        if not env:
            tmp_env = os.getenv("ORIGO_ENVIRONMENT", None)
            if tmp_env:
                env = tmp_env
        if env not in ORIGO_CONFIG:
            env = ORIGO_DEFAULT_ENVIRONMENT
        return env

    def get(self, key):
        if key in self.config:
            return self.config[key]
        raise ConfigurationError(f"No such key: {key}")

    def create_config_type(self, type, env):
        log.info(f"SDK:Creating config: {type} for {env}")
        if type == "environment":
            return EnvironmentConfig.create(env)
        if type == "configuration":
            return ConfigurationConfig.create(env)
        return False

    def create_config(self, env):
        config = EnvironmentConfig.create(env)
        if config is not False:
            return config

        config = ConfigurationConfig.create(env)
        if config is not False:
            return config

        return False


class EnvironmentConfig:
    def resolve_environment(env):
        if not env:
            env = ORIGO_DEFAULT_ENVIRONMENT
        if env not in ORIGO_CONFIG:
            env = ORIGO_DEFAULT_ENVIRONMENT
        return env

    def create(env):
        log.info(f"SDK:Creating EnvironmentConfig for {env}")
        env = EnvironmentConfig.resolve_environment(env)
        conf = ORIGO_CONFIG[env]
        # Map environment variables to internal configuration structure
        envConf = {
            "ORIGO_CLIENT_ID": "client_id",
            "ORIGO_CLIENT_SECRET": "client_secret",
            "ORIGO_USERNAME": "username",
            "ORIGO_PASSWORD": "password",
        }
        for key in envConf.keys():
            value = os.getenv(key, default=None)
            if value is None:
                log.info(f"Could not resolve value for {key}")
                continue
            conf[envConf[key]] = value
        return conf


class ConfigurationConfig:
    def create(env):
        log.info(f"SDK:Creating ConfigurationConfig for {env}")
        return False
