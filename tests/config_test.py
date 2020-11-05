from okdata.sdk.config import Config, EnvironmentConfig, OKDATA_DEFAULT_ENVIRONMENT
from okdata.sdk.exceptions import ConfigurationError


class TestConfig:
    def test_config_get_existing_key(self):
        config = Config(type="environment")
        # ENV variables set in tox.ini
        assert config.get("client_id") == "my-okdata-user"
        assert config.get("client_secret") == "my-okdata-password"

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
        env = EnvironmentConfig.resolve_environment(OKDATA_DEFAULT_ENVIRONMENT)
        assert env == OKDATA_DEFAULT_ENVIRONMENT
        env = EnvironmentConfig.resolve_environment("foobar")
        assert env == OKDATA_DEFAULT_ENVIRONMENT
        env = EnvironmentConfig.resolve_environment(None)
        assert env == OKDATA_DEFAULT_ENVIRONMENT

    def test_okdata_env_variables(self, monkeypatch):
        monkeypatch.setenv("OKDATA_CLIENT_ID", "veryniceuser")
        config = EnvironmentConfig.create(OKDATA_DEFAULT_ENVIRONMENT)
        assert config["client_id"] == "veryniceuser"
