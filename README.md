[![PyPI](https://img.shields.io/pypi/v/okdata-sdk)](https://pypi.org/project/okdata-sdk/)

# `okdata-sdk`: Python SDK for Origo Dataplatform

[`okdata-sdk`](https://pypi.org/project/okdata-sdk/) is on PyPI: `pip install okdata-sdk`

# Configuration

When calling any classes interacting with the Origo Dataplatform API and there are no Config params passed to the constructor, a config object will be
automaticly created for you based on environment variables


### Environment variables
Default, will pick up configuration from current environment.
The credentials is resolved automatically if you do not set a specific Auth config, in the following order:

1. _Client Credentials_: If you have added client_id / client_secret to the config. Or if you use the
environment variable equivalent: `OKDATA_CLIENT_ID` / `OKDATA_CLIENT_SECRET`.
2. _Username And Password_:  If you have added username / password to the config. Or if you use the
environment variable equivalent: `OKDATA_USERNAME` / `OKDATA_PASSWORD`.
```
# keycloak user
export OKDATA_USERNAME=my-user

# keycloak password for OKDATA_USERNAME
export OKDATA_PASSWORD=my-password

# keycloak client
export OKDATA_CLIENT_ID=my-machine-client

# keycloak secret for OKDATA_CLIENT_ID
export OKDATA_CLIENT_SECRET=some-generated-secure-string


# overrides default environment (dev), but will be trumped by --env=<environment> on the commandline
export OKDATA_ENVIRONMENT=dev|prod

# If you are sending events and have been assigned a API key
export OKDATA_API_KEY=your-api-key
```

### Getting Credentials:
`username/password ` are synced with Oslo municipalities Active Directory so any user with an association can
use their personal account to access the SDK.

For `client credentials` please contact the data platform team. `dataplattform[at]oslo.kommune.no`

### TODO: Named profiles
If environment variables are not available, the system will try to load from a default profile: Located in ~/.okdata/configuration

# Usage

Table of contents:
- [Upload data](#upload-data)
- [Download data](#download-data)
- [Creating datasets with versions and editions](#creating-datasets-with-versions-and-editions)
- [Updating dataset metadata](#updating-dataset-metadata)

## Upload data

When uploading data you need to refer to an existing dataset that you own, a version and an edition.
If these are non existent then you can create them yourself. This can be achieved [using the sdk](#creating-datasets-with-versions-and-editions),
or you can use our [command line interface](https://github.com/oslokommune/okdata-cli).


```python
from okdata.sdk.data.upload import Upload
from okdata.sdk.config import Config

okdata_config = Config()

# If necessary you can override default values
okdata_config.config["cacheCredentials"] = False

data_uploader = Upload(config=okdata_config)

# Upload file 'data.json' to dataset-id/version/edition
dataset_id = "my-dataset-id"
version = "my-version"  # example value: 1
edition = "my-edition"  # example value: 20200618T114038

filename = "/path-to-file/data.json"

# Note! filename must be pointing to an existing file on your disk
upload_response = data_uploader.upload(filename, dataset_id, version, edition)
print(upload_response)
# {
#     "result": True,
#     "trace_id": "my-dataset-id-54a3c78e-86a3-4631-8f28-0252fe1c7c13"
# }
```

The `trace_id` returned by the upload method can be used to "trace" the steps involved in the upload process:

```python
from okdata.sdk.status import Status
...
status = Status(config=okdata_config)
trace_events = status.get_status(trace_id)
print(trace_events)
# [
#     {
#         "trace_id": "my-dataset-1a2bc345-6789-1234-567d-8912ef34a567",
#         "trace_status": "STARTED",
#         "trace_event_id": "1a2b3cd4-eef5-6aa7-bccd-e889912334f5",
#         "trace_event_status": "OK",
#         "component": "data-uploader",
#         ...
#     },
#     {
#         "trace_id": "my-dataset-1a2bc345-6789-1234-567d-8912ef34a567",
#         "trace_status": "CONTINUE",
#         ...
#     },
#     {
#         "trace_id": "my-dataset-1a2bc345-6789-1234-567d-8912ef34a567",
#         "trace_event_id": "1aa2b345-678c-9de1-f2a3-4566bcd78912",
#         "trace_status": "FINISHED",
#         "trace_event_status": "OK",
#         ...
#     }
# ]
```

## Download data

To download data you need to refer to a dataset that you have access to. This
could be a public dataset, a restricted dataset you've been given access to, or
a dataset that you own yourself. If the dataset is public, [authenticating
yourself](#environment-variables) is not necessary.

You will also need to refer to the specific version and edition of the dataset
that you want to download. If this is your own dataset, make sure to create a
[version and edition](#creating-datasets-with-versions-and-editions) before
attempting to download it.

```python
from okdata.sdk.data.download import Download
from okdata.sdk.config import Config

okdata_config = Config(env="dev")

# If necessary you can override default config values
okdata_config.config["cacheCredentials"] = False

data_downloader = Download(config=okdata_config)

dataset_id = "your-dataset-id"
version = "1"
edition = "latest"

# Downloading a file
res1 = data_downloader.download(dataset_id, version, edition, "my/preferred/output/path")
print(res1)
# {
#     "downloaded_files": ["my/preferred/output/path/file_name.csv"]
# }
```

## Creating datasets with versions and editions
```python
from okdata.sdk.data.dataset import Dataset
from okdata.sdk.config import Config

okdata_config = Config()

# If necessary you can override default values
okdata_config.config["cacheCredentials"] = False

# Create a new dataset
dataset = Dataset(config=okdata_config)

dataset_metadata = {
    "title": "Precise Descriptive Title",
    "description": "Describe your dataset here",
    "keywords": ["some-keyword"],
    "accessRights": "public",
    "objective": "Exemplify how to create a new dataset",
    "contactPoint": {
        "name": "Your name",
        "email": "your_email@domain.com",
        "phone": "999555111"
    },
    "publisher": "name of organization or person responsible for publishing the data"
}

new_dataset = dataset.create_dataset(data=dataset_metadata)

# new_dataset:
# { 'Id': 'precise-descriptive-title',
#   'Type': 'Dataset',
#   '_links': {'self': {'href': '/datasets/precise-descriptive-title'}},
#   'accessRights': 'public',
#   'contactPoint': { 'email': 'your_email@domain.com',
#                     'name': 'Your name',
#                     'phone': '999555111'},
#   'description': 'Describe your dataset here',
#   'keywords': ['some-keyword'],
#   'objective': 'Exemplify how to create a new dataset',
#   'publisher': 'name of organization or person responsible for publishing the '
#                'data',
#   'title': 'Precise Descriptive Title'}


# create version for new dataset:
version_data = {"version": "1"}
new_version = dataset.create_version(new_dataset["Id"], data=version_data)

# new_version:
# { 'Id': 'precise-descriptive-title/1',
#   'Type': 'Version',
#   '_links': { 'self': { 'href': '/datasets/precise-descriptive-title/versions/1'}},
#   'version': '1'}

# create edition for new_dataset/new_version:
import datetime

# Note! edition-field must be ISO 8601 with utc offset
edition_data = {
    "edition": str(datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()),
    "description": "My edition description",
    "startTime": "2019-01-01",
    "endTime": "2019-12-31"
}
new_edition = dataset.create_edition(new_dataset["Id"], new_version["version"], data=edition_data)

# new_edition
# { 'Id': 'precise-descriptive-title/1/20200115T130439',
#   'Type': 'Edition',
#   '_links': { 'self': { 'href': '/datasets/precise-descriptive-title/versions/1/editions/20200115T130439'}},
#   'description': 'My edition description',
#   'edition': '2020-01-15T13:04:39.041778+00:00',
#   'endTime': '2019-12-31',
#   'startTime': '2019-01-01'}
```

## Updating dataset metadata

Similarly to creating datasets, metadata for any given dataset, version etc., can also be
**updated** by using the methods listed below. These methods accept an updated version of
the JSON document posted when creating the same resource:

```py
dataset.update_dataset(datasetid, data={ ... })
dataset.update_version(datasetid, versionid, data={ ... })
dataset.update_edition(datasetid, versionid, editionid, data={ ... })
dataset.update_distribution(datasetid, versionid, editionid, distributionid, data={ ... })

# Example: Update dataset metadata
dataset.update_dataset(
    datasetid="precise-descriptive-title",
    data={
        "title": "Precise Descriptive Title",
        "description": "Describe your dataset here",
        "keywords": ["some-keyword", "another-keyword"], # Add another keyword
        "accessRights": "public",
        "license": "http://data.norge.no/nlod/", # Add licensing information
        "objective": "Exemplify how to update an existing dataset", # Update objective text
        "contactPoint": {
            "name": "Your name",
            "email": "your_email@domain.com",
            "phone": "999555111"
        },
        "publisher": "name of organization or person responsible for publishing the data"
    }
)
```

The `update_dataset` method also supports an optional `partial` keyword,
enabling partial updates when true:

```py
dataset.update_dataset(
    "my-dataset-id", {"description": "Only update description"}, partial=True
)
```
