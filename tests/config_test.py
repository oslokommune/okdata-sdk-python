from origo.sdk.config import Config, EnvironmentConfig, ORIGO_DEFAULT_ENVIRONMENT
from origo.sdk.exceptions import ConfigurationError


class TestConfig:
    def test_config_get_existing_key(self):
        config = Config(type="environment")
        assert config.get("client_id") == "my-origio-user"
        assert config.get("client_secret") == "my-origo-password"

    def test_config_get_non_existing_key(self):
        config = Config(type="environment")
        try:
            config.get("non-existing-key")
            assert False
        except ConfigurationError:
            assert True

    def test_create_invalid_configuration(self):
        try:
            Config(type="foobar")
            assert False
        except ConfigurationError:
            assert True

    def test_custom_config(self):
        custom_config = {"foo": "omg this cake tastes so good", "bar": "give me cheese"}
        config = Config(config=custom_config)
        assert config.config == custom_config


class TestEnvironmentConfig:
    def test_resolve_environment(self):
        env = EnvironmentConfig.resolve_environment(ORIGO_DEFAULT_ENVIRONMENT)
        assert env == ORIGO_DEFAULT_ENVIRONMENT
        env = EnvironmentConfig.resolve_environment("foobar")
        assert env == ORIGO_DEFAULT_ENVIRONMENT
        env = EnvironmentConfig.resolve_environment(None)
        assert env == ORIGO_DEFAULT_ENVIRONMENT
