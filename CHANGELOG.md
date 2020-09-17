## 0.2.5

* Rename event stream methods:
    * `enable_subscribable` > `enable_subscription`
    * `disable_subscribable` > `disable_subscription`
    * `add_sink` > `enable_sink`
    * `remove_sink` > `disable_sink`

## 0.2.4

* Add event stream API support.

## 0.2.3

* Use the same default value for `cacheCredentials` in both development and
  production environments.
* Update Makefile for better Python 3 compatibility.

## 0.2.2

* Add function for downloading data.
* Call `raise_for_status()` when not using SDK class.
* Reintroduce Python 3.6 support.

## 0.2.1

* Check if `refresh token` is expired before calling
  `KeycloakOpenID.refresh_token()`.

## 0.2.0

* Change default environment to production.
* Add `simple-dataset-authorizer`.

## 0.1.0

* Get default value from `s3SignedData` if it doesn't exist.
* Return both status and status ID for uploads to a dataset.
* Add support for `taskConfig`.
* Add support for status API.

## 0.0.19

* Remove `DataExistError`.
* Use `self.post()` in `PostEvent`.
* Use `response.raise_for_status()` as sole error handling in SDK.

## 0.0.18

* Use `python-keycloak`.

## 0.0.17

* Use API gateway mapped URL for Elasticsearch queries.
* Add Elasticsearch queries SDK.

## 0.0.16

* Update documentation with new code examples and structure.

## 0.0.15

* Add stream manager to SDK.

## 0.0.14

* Distribute JSON schemas for pipeline inputs and schemas.

## 0.0.13

* *No changes*

## 0.0.12

* Schema bugfix.
* Fix homepage URL in `setup.py`.

## 0.0.11

* Add schema.
* Add code examples for creating datasets, uploading files, and sending events.
* Move developer documentation to separate file.
* Add support for pipeline input.

## 0.0.10

* Update README.
* Export schema for pipeline and instance.

## 0.0.9

* Add possibility to create distribution via API.

## 0.0.8

* Use correct production value for `s3BucketUrl`.
* Use correct resource name for pipeline instances.
* Update tests to match new filter implementation.
* Add filter possibilities on dataset list.
* Add helpers for pipeline API.
* Add pipeline instances to SDK client.
* Add pipeline API SDK client for pipelines.

## 0.0.7

* Run `is-git-clean` before `bump-patch`.
* Add constructor argument for custom configuration object.

## 0.0.6

* Use correct production URLs.

## 0.0.5

* Add `__init__.py` to `event` module.

## 0.0.4

* *No changes*

## 0.0.3

* Include all packages, but exclude tests, in `setup.py`.
* Bump version before building.
* Automatic tests with GitHub Actions.

## 0.0.2

* Add make targets for publishing to PyPI.
* Add classifiers for license.

## 0.0.1

* Initial release.