from okdata.sdk import SDK


class SimpleDatasetAuthorizerClient(SDK):
    def __init__(self, config=None, auth=None, env=None):
        self.__name__ = "simple_dataset_authorizer"
        super().__init__(config, auth, env)
        self.dataset_authorizer_url = self.config.get("simpleDatasetAuthorizerUrl")

    def create_dataset_access(
        self, dataset_id, prinical_id, bearer_token=None, retries=0
    ):
        create_dataset_access_url = f"{self.dataset_authorizer_url}/{dataset_id}"
        request_data = {"principalId": prinical_id}
        if bearer_token:
            result = self.prepared_request_with_retries(retries).post(
                create_dataset_access_url,
                headers={"Authorization": f"Bearer {bearer_token}"},
                data=request_data,
            )
            result.raise_for_status()
            return result.json()
        return self.post(
            create_dataset_access_url, data=request_data, retries=retries
        ).json()

    def check_dataset_access(self, dataset_id, bearer_token=None, retries=0):
        check_dataset_access_url = f"{self.dataset_authorizer_url}/{dataset_id}"
        if bearer_token:
            result = self.prepared_request_with_retries(retries).get(
                check_dataset_access_url,
                headers={"Authorization": f"Bearer {bearer_token}"},
            )
            result.raise_for_status()
            return result.json()
        return self.get(check_dataset_access_url, retries=retries).json()

    def create_webhook_token(self, dataset_id, service_name, retries=0):
        response = self.post(
            f"{self.dataset_authorizer_url}/{dataset_id}/webhook",
            data={"service": service_name},
            retries=retries,
        )
        return response.json()

    def list_webhook_tokens(self, dataset_id, retries=0):
        response = self.get(
            f"{self.dataset_authorizer_url}/{dataset_id}/webhook", retries=retries
        )

        return response.json()

    def delete_webhook_token(self, dataset_id, webhook_token, retries=0):
        response = self.delete(
            f"{self.dataset_authorizer_url}/{dataset_id}/webhook/{webhook_token}",
            retries=retries,
        )
        return response.json()

    def authorize_webhook_token(self, dataset_id, webhook_token, retries=0):
        response = self.get(
            f"{self.dataset_authorizer_url}/{dataset_id}/webhook/{webhook_token}/authorize",
            retries=retries,
        )
        return response.json()
