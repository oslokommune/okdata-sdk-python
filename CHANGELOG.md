## 2.4.0

* Added support for Python 3.11.

## 2.3.0

* New method `TeamClient.get_user_by_username` for looking up Keycloak users.
* New method `TeamClient.update_team_members` for adding and/or removing
  members to/from a team.

## 2.2.1

* Fixed a bug in `TeamClient.update_team_attribute` when `value` is falsy.

## 2.2.0

* New parameter `include` added to `TeamClient.get_teams`.
* New method `TeamClient.get_team_members` for getting the members of a team.
* New methods `TeamClient.update_team_name` and
  `TeamClient.update_team_attribute` for updating team names and their
  attributes, respectively.

## 2.1.0

* New method `TeamClient.get_team_by_name`.
* Fixed a deprecation warning from urllib3.

## 2.0.0

* A new client class `TeamClient` for retrieving information about teams has
  been added.
* The classes `PostEvent`, `EventStreamClient`, and `ElasticsearchQueries` for
  working with event streams have all been removed.
* The `WebhookClient` class for managing webhooks has been removed.
* The `SimpleDatasetAuthorizerClient` class was deprecated and has been removed.

## 1.0.0

* Added support for Python 3.10.
* Dropped support for Python 3.6.

## 0.9.2

* Use built-in JSON encoder from `requests` for `post`, `put` and `patch` methods.

## 0.9.1

* Handle error responses from status API update calls.

## 0.9.0

* Tweaked the webhook client to create and authorize tokens based on operations
  (read, write) instead of tying them to a specific service.

## 0.8.2

* Add new SDK `WebhookClient` for managing webhook tokens with okdata-permission-api.

## 0.8.1

* Fix handling of Keycloak tokens that don't contain a refresh token.

## 0.8.0

* Added support for the new [permission API](https://github.com/oslokommune/okdata-permission-api).

* Retries have been re-enabled for low-level network errors (connection errors,
  read errors, and redirects). The `retry` parameter now only controls the
  maximum number of retries to perform on bad HTTP status codes.

* Fix refresh of Keycloak access token when refresh token is invalid, e.g.
  due to inactive session because Keycloak server restarted.

## 0.7.0

* `Dataset.update_dataset` now supports partial metadata updates when the
  keyword argument `partial` is true.

## 0.6.3

* PyJWT 2.0.0 or above is now required.

## 0.6.2

* Authentication is no longer necessary for downloading public ("green")
  datasets.

## 0.6.1

* `PostEvent.post_event` now also supports retries.

## 0.6.0

* Added `Dataset.get_distribution` method.
* Added `Dataset.update_*` methods for updating dataset, version, edition and
  distribution metadata.
* Added retry parameter to SDK methods.
* The `confidentiality` metadata field is now fully replaced by `accessRights`.

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
