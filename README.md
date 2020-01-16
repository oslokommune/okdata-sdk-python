# Configuration

When calling any classes interacting with the Origo API and there are no Config params passed to the constructor, a config object will be
automaticly created for you based on environment variables


### Environment variables
Default, will pick up configuration from current environment.
The credentials is resolved automatically if you do not set a specific Auth config, in the following order:

1. _Client Credentials_: If you have added client_id / client_secret to the config. Or if you use the
environment variable equivalent: `ORIGO_CLIENT_ID` / `ORIGO_CLIENT_SECRET`.
2. _Username And Password_:  If you have added username / password to the config. Or if you use the
environment variable equivalent: `ORIGO_USERNAME` / `ORIGO_PASSWORD`.
```
# keycloak user
export ORIGO_USERNAME=my-user

# keycloak password for ORIGO_USERNAME
export ORIGO_PASSWORD=my-password

# keycloak client
export ORIGO_CLIENT_ID=my-machine-client

# keycloak secret for ORIGO_CLIENT_ID
export ORIGO_CLIENT_SECRET=some-generated-secure-string


# overrides default environment (dev), but will be trumped by --env=<environment> on the commandline
export ORIGO_ENVIRONMENT=dev|prod

# If you are sending events and have been assigned a API key
export ORIGO_API_KEY=your-api-key
```

### Getting Credentials:
`username/password ` are synced with Oslo municipalities Active Directory so any user with an association can
use their personal account to access the SDK.

For `client credentials` please contact the data platform team. `dataplattform[at]oslo.kommune.no`

### TODO: Named profiles
If environment variables are not available, the system will try to load from a default profile: Located in ~/.origo/configuration

# Usage

## Upload data

When uploading data you need to refer to an existing dataset that you own, a version and an edition. 
If these are non existent then you can create them yourself. This can be achieved [using the sdk](#create-a-new-dataset-with-version-and-edition),
or you can use our [command line interface](https://github.com/oslokommune/origo-cli).


```python
from origo.data.upload import Upload
from origo.config import Config

origo_config = Config()

# If necessary you can override default values
origo_config.config["cacheCredentials"] = False

data_uploader = Upload(config=origo_config)

# Upload file 'data.json' to dataset-id/version/edition
dataset_id = "your-dataset-id"
version = "version"
edition = "20200115T130439"

filename = "data.json"

# Note! filename must be pointing to an existing file on your disk
upload_success = data_uploader.upload(filename, dataset_id, version, edition)
```

## Sending events

Before you can start sending events you need to have defined a dataset and a version.
This can be achieved [using the sdk](#create-a-new-dataset-with-version-and-edition),
or you can use our [command line interface](https://github.com/oslokommune/origo-cli).
You not need to define an edition in order to send events. However you need to set up
an event-stream. As for now you have to contact Team Dataplattform at Origo in order
to set up an event-stream.

```python
from origo.event.post_event import PostEvent
from origo.config import Config

origo_config = Config()

# If necessary you can override default config values
origo_config.config["cacheCredentials"] = True

event_poster = PostEvent(config=origo_config)

dataset_id = "some-dataset-id"
version = "1"
event = {"foo": "bar"}

res = event_poster.post_event(event, dataset_id, version)
# res:
# {'message': 'Ok'}

# Method also supports list of dictionaries
event_list = [{"foo": "bar"}, {"foo": "bar"}]

res2 = event_poster.post_event(event_list, dataset_id, version)
# res2:
# {'message': 'Ok'}

```


## Create a new dataset with version and edition
```python
from origo.data.dataset import Dataset
from origo.config import Config

origo_config = Config()

# If necessary you can override default values
origo_config.config["cacheCredentials"] = False

# Create a new dataset
dataset = Dataset(config=origo_config)

dataset_metadata = {
    "title": "Precise Descriptive Title",
    "description": "Describe your dataset here",
    "keywords": ["some-keyword"],
    "accessRights": "public",
    "confidentiality": "green",
    "objective": "Exemplify how to create a new dataset",
    "contactPoint": {
        "name": "Your name",
        "email": "your_email@domain.com",
        "phone": "999555111"
    },
    "publisher": "name of organization or person responsible for publishing the data",
    "processing_stage": "raw"
}

new_dataset = dataset.create_dataset(data=dataset_metadata)

# new_dataset:
# { 'Id': 'precise-descriptive-title',
#   'Type': 'Dataset',
#   '_links': {'self': {'href': '/datasets/precise-descriptive-title'}},
#   'accessRights': 'public',
#   'confidentiality': 'green',
#   'contactPoint': { 'email': 'your_email@domain.com',
#                     'name': 'Your name',
#                     'phone': '999555111'},
#   'description': 'Describe your dataset here',
#   'keywords': ['some-keyword'],
#   'objective': 'Exemplify how to create a new dataset',
#   'processing_stage': 'raw',
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