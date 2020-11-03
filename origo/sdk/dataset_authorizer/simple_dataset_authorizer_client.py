import requests

from origo.sdk import SDK


class SimpleDatasetAuthorizerClient(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "simple_dataset_authorizer"
        super().__init__(config, auth, env)
        self.dataset_authorizer_url = self.config.get("simpleDatasetAuthorizerUrl")

    def create_dataset_access(self, dataset_id, prinical_id, bearer_token=None):
        create_dataset_access_url = f"{self.dataset_authorizer_url}/{dataset_id}"
        request_data = {"principalId": prinical_id}
        if bearer_token:
            result = requests.post(
                create_dataset_access_url,
                headers={"Authorization": f"Bearer {bearer_token}"},
                data=request_data,
            )
            result.raise_for_status()
            return result.json()
        return self.post(create_dataset_access_url, data=request_data).json()

    def check_dataset_access(self, dataset_id, bearer_token=None):
        check_dataset_access_url = f"{self.dataset_authorizer_url}/{dataset_id}"
        if bearer_token:
            result = requests.get(
                check_dataset_access_url,
                headers={"Authorization": f"Bearer {bearer_token}"},
            )
            result.raise_for_status()
            return result.json()
        return self.get(check_dataset_access_url).json()

    def create_webhook_token(self, dataset_id, service_name):
        response = self.post(
            f"{self.dataset_authorizer_url}/{dataset_id}/webhook",
            data={"service": service_name},
        )
        return response.json()

    def list_webhook_tokens(self, dataset_id):
        response = self.get(f"{self.dataset_authorizer_url}/{dataset_id}/webhook")

        return response.json()

    def delete_webhook_token(self, dataset_id, webhook_token):
        response = self.delete(
            f"{self.dataset_authorizer_url}/{dataset_id}/webhook/{webhook_token}"
        )
        return response.json()

    def authorize_webhook_token(self, dataset_id, webhook_token):
        response = self.get(
            f"{self.dataset_authorizer_url}/{dataset_id}/webhook/{webhook_token}/authorize"
        )
        return response.json()
