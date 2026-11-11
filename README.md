[![PyPI](https://img.shields.io/pypi/v/okdata-sdk)](https://pypi.org/project/okdata-sdk/)

# `okdata-sdk`: Python SDK for Oslo kommune data services

[`okdata-sdk`](https://pypi.org/project/okdata-sdk/) is on PyPI and requires
Python 3.11 or newer:

```sh
pip install okdata-sdk
```

## Configuration

Credentials are resolved automatically in the following order:

1. _Client credentials_: If you have added `client_id`/`client_secret` to the
   config, or if you use the environment variable equivalents
   `OKDATA_CLIENT_ID`/`OKDATA_CLIENT_SECRET`.
2. _Username and password_: If you have added `username`/`password` to the
   config, or if you use the environment variable equivalents
   `OKDATA_USERNAME`/`OKDATA_PASSWORD`.

```sh
# Client ID
export OKDATA_CLIENT_ID=my-machine-client

# Client secret for `OKDATA_CLIENT_ID`
export OKDATA_CLIENT_SECRET=some-generated-secure-string

# Personal Active Directory (AD) username
export OKDATA_USERNAME=my-user

# Password for `OKDATA_USERNAME`
export OKDATA_PASSWORD=my-password

# Overrides the default environment (prod)
export OKDATA_ENVIRONMENT=dev|prod
```

### Getting credentials

Usernames and passwords are synced with Oslo kommune's Active Directory, so
anyone with an AD account can use their personal credentials with the SDK.

If you need client credentials, please contact Dataspeilet at
`dataspeilet@oslo.kommune.no`.

## Usage

All client classes accept optional `config` and `env` arguments. When `config`
is omitted, a `Config` object is created automatically from the environment
variables described above, and `env` selects the environment, either `"dev"` or
`"prod"` (the default):

```python
from okdata.sdk.team.client import TeamClient

team_client = TeamClient(env="dev")
```

### Permissions

Resource names have the form `namespace:type:id`, and scopes have the form
`namespace:type:permission`.

```python
from okdata.sdk.permission.client import PermissionClient
from okdata.sdk.permission.user_types import Client, Team, User

permission_client = PermissionClient()

# List the permissions associated with the current user
my_permissions = permission_client.get_my_permissions()
# {
#     "maskinporten:client:my-client-id": {"scopes": ["maskinporten:client:read"]},
#     ...
# }

# List the permissions associated with a resource
permissions = permission_client.get_permissions("maskinporten:client:my-client-id")

# Grant read access to the user "janedoe" and the team with ID "my-team-id",
# and revoke it from the Keycloak client "my-keycloak-client"
permission_client.update_permission(
    "maskinporten:client:my-client-id",
    "maskinporten:client:read",
    add_users=[User("janedoe"), Team("my-team-id")],
    remove_users=[Client("my-keycloak-client")],
)
```

### Teams

```python
from okdata.sdk.team.client import TeamClient

team_client = TeamClient()

# List the teams the current user is a member of
my_teams = team_client.get_teams()

# List all teams regardless of membership, optionally filtered by role
all_teams = team_client.get_teams(include="all")
teams_with_role = team_client.get_teams(include="all", has_role="my-role")

# Look up a single team by ID or name
team = team_client.get_team("my-team-id")
team = team_client.get_team_by_name("My Team")

# List and replace the members of a team
members = team_client.get_team_members("my-team-id")
members = team_client.update_team_members("my-team-id", ["janedoe", "johndoe"])

# Update a team's name or one of its attributes (a falsy value removes the
# attribute)
team_client.update_team_name("my-team-id", "My Renamed Team")
team_client.update_team_attribute("my-team-id", "email", "my-team@example.com")

# Look up a Keycloak user by username
user = team_client.get_user_by_username("janedoe")
```

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for how to set up a development
environment, run the tests, and release a new version.
