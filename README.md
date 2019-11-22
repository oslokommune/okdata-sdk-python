# Usage

See the origo-cli repo for implementation and usage of the SDK

## Configuration

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

## Run
```
git clone git@github.oslo.kommune.no:origo-dataplatform/origo-sdk-python.git
cd origo-sdk-python
python3.7 -m venv .venv
. .venv/bin/activate
make init
```

# Development

## Getting started

Run all tests:
```
$ make test
```

Reformat files:
```
make format
```
