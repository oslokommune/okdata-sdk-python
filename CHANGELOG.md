## 0.5.3

* Added `Dataset.get_distribution` method
* Added `Dataset.update_*` methods for updating dataset, version, edition and distribution metadata
* Added retry parameter to sdk methods

## 0.5.2

* The `okdata` namespace package now uses the old-style `pkg_resources`
  declaration instead of being an implicit namespace package.

## 0.5.1

* Added `Status.update_status` method

## 0.5.0

### Breaking

* Rename project to `okdata-sdk`.
    - Repository name will be `okdata-sdk-python`
    - PyPI package `okdata-sdk`
    - Python modules will reside in `okdata.sdk.*`, where `okdata` is an
      implicit namespace.

## 0.4.0

### Breaking

* Modules reorganized to leave top level `origo` namespace empty, all modules
  are now under `origo.sdk`. Ie. `from origo.data.upload import Upload` now
  becomes `from origo.sdk.data.upload import Upload`. This allows other
  packages to add their modules under the `origo` namespace.

## 0.3.0

* Support the new status API response format. This affects the upload command
  response, now returning a `trace_id` key instead of `status`.

* `PipelineInstance` now takes an optional parameter `pipelineProcessorId`,
  intended to supersede `pipelineArn` once all users have been updated. The
  `pipelineArn` parameter is now optional.

* The `taskConfig` to `PipelineInstance` is now also optional.

* `PipelineInstance` no longer accepts the obsolete parameters `schemaId`,
  `transformation`, and `useLatestEdition`.

## 0.2.7

* Enable, disable and get event stream sinks by *type* (not id).

## 0.2.6

* Add function for listing webhook tokens for a dataset.

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
