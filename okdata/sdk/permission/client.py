import logging
from dataclasses import asdict
from urllib.parse import quote

from okdata.sdk import SDK

log = logging.getLogger()


class PermissionClient(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "permission"
        super().__init__(config, auth, env)
        self.api_url = self.config.get("permissionApiUrl")

    def update_permission(
        self, resource_name, scope, add_users=[], remove_users=[], retries=0
    ):
        """Grant or revoke permissions for a resource.

        `resource_name` must be given on the form "namespace:type:id", while
        `scope` must be given on the form "namespace:type:permission".

        `add_users` and `remove_users` are iterables containing the users to
        give access to and to revoke access from, respectively. The users
        should be instances of the user types defined in
        `okdata.sdk.permission.user_types`.

        Usage example giving read access to the dataset "my-dataset" to the
        user "janedoe":

          update_permission(
              "okdata:dataset:my-dataset",
              "okdata:dataset:read",
              add_users=[User("janedoe")],
          )
        """
        url = "{}/permissions/{}".format(self.api_url, quote(resource_name))
        data = {
            "add_users": list(map(asdict, add_users)),
            "remove_users": list(map(asdict, remove_users)),
            "scope": scope,
        }
        log.info(f"SDK:Updating permissions for {resource_name} with {data}")
        return self.put(url, data, retries=retries).json()

    def get_my_permissions(self, retries=0):
        """Return a dictionary of permissions associated with the current user.

        The dictionary is on the form:

          {
            "resource-name-1": {"scopes": ["scope-1", "scope-2"]},
            "resource-name-2": ...
          }
        """
        url = f"{self.api_url}/my_permissions"
        log.info(f"SDK:Listing permissions from: {url}")
        return self.get(url, retries=retries).json()

    def get_permissions(self, resource_name, retries=0):
        """Return a list of permissions associated with `resource_name`."""
        url = "{}/permissions/{}".format(self.api_url, quote(resource_name))
        log.info(f"SDK:Getting permissions for {resource_name} from: {url}")
        return self.get(url, retries=retries).json()
