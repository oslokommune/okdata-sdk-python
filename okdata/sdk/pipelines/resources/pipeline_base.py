import json
import os
from typing import Tuple, Optional

import jsonschema  # type: ignore
from jsonschema import ValidationError, SchemaError
from requests import HTTPError

from okdata.sdk import SDK


class InternalError(Exception):
    pass


class ResourceConflict(Exception):
    pass


class PipelineBase:
    """An abstract class for resources in pipeline-api

    Attributes:
        sdk: An instance of the SDK
    """

    sdk: SDK
    __resource_name__: str

    def __init__(self, *args, **kwargs):
        raise NotImplementedError()

    def validate(self) -> Tuple[bool, Optional[ValidationError]]:
        """Validates the current object against a json schema

        Uses __resource_name__ to find the correct schema

        Returns: Tuple of: Bool (valid), ValidationError if any

        """
        path = os.path.dirname(__file__)
        with open(f"{path}/schemas/{self.__resource_name__}.json") as f:
            try:
                jsonschema.validate(self.__dict__, json.loads(f.read()))
                return True, None
            except SchemaError:
                # TODO: Logging
                raise InternalError
            except ValidationError as ve:
                # TODO: Logging
                return False, ve

    def create(self) -> Tuple[Optional[str], Optional[HTTPError]]:
        """Creates the current object in pipeline-api

        Uses __resource_name__ to create the post url
        Validates the current object first

        Returns: Tuple of: String with the resource ID, HTTPErrors if any

        """
        valid, error = self.validate()
        if error and not valid:
            raise error
        base_url = self.sdk.config.get("pipelineUrl")
        url = f"{base_url}/{self.__resource_name__}"

        try:
            return self.sdk.post(url=url, data=self.__dict__).text.strip(), None
        except HTTPError as he:
            return None, he

    def _valid_and_exists(self):
        valid, error = self.validate()
        if error and not valid:
            raise error
        if self.exists():
            raise ResourceConflict
        return valid

    @classmethod
    def from_dict(cls, sdk: SDK, instance_dict: dict):
        """Create a pipeline resource from a dictionary

        Args:
            sdk: An instance of the sdk
            instance_dict: dict Must contain the exact keywords for a class' __init__ function

        Returns: An pipeline resource instance

        """
        return cls(sdk, **instance_dict)

    @classmethod
    def from_id(cls, sdk: SDK, id: str):
        """Fetch a resource from pipeline-api using an ID

        Args:
            sdk: An instance of the sdk
            id: str Some id used to look up the corresponding resource. E.g. ARN for Pipeline or Id for PipelineInstance

        Returns: An pipeline resource instance

        """
        data = sdk.get(
            sdk.config.get("pipelineUrl") + f"/{cls.__resource_name__}/{id}"
        ).json()
        return cls.from_dict(sdk, data)

    @classmethod
    def from_json(cls, sdk: SDK, resource: str):
        """Create a pipeline resource from string

        Args:
            sdk: An instance of the sdk
            resource: dict Must contain the exact keywords for a class' __init__ function

        Returns: An pipeline resource instance

        """
        data = json.loads(resource)
        return cls.from_dict(sdk, data)

    @classmethod
    def _exists(cls, sdk, id):
        url = sdk.config.get("pipelineUrl")
        result = sdk.get(url=f"{url}/{cls.__resource_name__}/{id}")
        return result.status_code == 200

    def exists(self):
        raise NotImplementedError

    @classmethod
    def _delete(cls, sdk: SDK, id: str):
        base_url = sdk.config.get("pipelineUrl")
        url = f"{base_url}/{cls.__resource_name__}/{id}"
        return sdk.delete(url=url).text.strip("'")

    def delete(self):
        raise NotImplementedError

    @classmethod
    def list(cls, sdk: SDK):
        """List instances of this pipeline resource

        Args:
            sdk: An instance of the sdk

        Returns: A list of pipeline resource instances
        """
        base_url = sdk.config.get("pipelineUrl")
        url = f"{base_url}/{cls.__resource_name__}"
        return sdk.get(url=url).json()

    def update(self):
        """Update the pipeline resource

        Since there is no update function for pipeline-api, we delete and recreate the resource.
        Asserts that the resource exists and that this object is valid.

        Returns: Id of the new resource
        """
        assert self.exists()
        valid, _ = self.validate()
        assert valid
        self.delete()
        return self.create()
