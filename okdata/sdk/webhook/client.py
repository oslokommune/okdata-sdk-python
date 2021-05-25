import logging

from okdata.sdk import SDK

log = logging.getLogger()


class WebhookClient(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "permission"
        super().__init__(config, auth, env)
        self.api_url = f"{self.config.get('permissionApiUrl')}/webhooks"

    def create_webhook_token(
        self, dataset_id: str, service_name: str, retries: int = 0
    ):
        """Create a webhook token associated with a dataset and an okdata service.

        Return a dictionary on the form:

          {
            "token": "774d8f35-fb4b-4e06-9d7f-54d1a08589b4",
            "created_by": "your-username",
            "dataset_id": "some-dataset",
            "service": "service-account-some-service",
            "created_at": "2020-02-29T00:00:00+00:00",
            "expires_at": "2022-02-28T00:00:00+00:00",
            "is_active": True,
          }
        Note!
        The service_name parameter should NOT be prefixed with "service-account-".
        """
        url = f"{self.api_url}/{dataset_id}/tokens"
        request_body = {"service": service_name}

        return self.post(url, request_body, retries=retries).json()

    def list_webhook_tokens(self, dataset_id: str, retries: int = 0):
        """List all webhook tokens associated with a dataset.

        Return a list of dictionaries on the form:
          [
            {
              "token": "774d8f35-fb4b-4e06-9d7f-54d1a08589b4",
              "created_by": "your-username",
              "dataset_id": "some-dataset",
              "service": "service-account-some-service",
              "created_at": "2020-02-29T00:00:00+00:00",
              "expires_at": "2022-02-28T00:00:00+00:00",
              "is_active": True,
            },
          .
          .
          ]
        """
        url = f"{self.api_url}/{dataset_id}/tokens"
        return self.get(url, retries=retries).json()

    def delete_webhook_token(self, dataset_id: str, token: str, retries: int = 0):
        """Delete a webhook token.

        Return a dictionary on the form:
          {
            "message": "Deleted token for dataset dataset_id"
          }
        """
        url = f"{self.api_url}/{dataset_id}/tokens/{token}"
        return self.delete(url, retries=retries).json()

    def authorize_webhook_token(self, dataset_id: str, token: str, retries: int = 0):
        """Check if a webhook token has access to perform operations on a dataset from a logged in service.

        Return a dictionary on the form:
          {
            "access": True
            "reason": None
          }
        """
        url = f"{self.api_url}/{dataset_id}/tokens/{token}/authorize"
        return self.get(url, retries=retries).json()
