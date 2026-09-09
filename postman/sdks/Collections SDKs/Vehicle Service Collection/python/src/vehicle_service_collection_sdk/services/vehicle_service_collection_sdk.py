from typing import Any, Optional, Union
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..net.sdk_config import SdkConfig
from ..net.environment.environment import Environment
from ..models.utils.cast_models import cast_models
from ..models import CreateAVehicleRequest


class VehicleServiceCollectionSdkService(BaseService):
    """
    Service class for VehicleServiceCollectionSdkService operations.
    Provides methods to interact with VehicleServiceCollectionSdkService-related API endpoints.
    Inherits common functionality from BaseService including authentication and request handling.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the service and method-level configurations."""
        super().__init__(*args, **kwargs)
        self._create_a_vehicle_config: SdkConfig = {}
        self._retrieve_a_vehicle_config: SdkConfig = {}
        self._update_a_collection_config: SdkConfig = {}
        self._delete_a_vehicle_config: SdkConfig = {}
        self._get_all_vehicles_config: SdkConfig = {}

    def set_create_a_vehicle_config(self, config: SdkConfig):
        """
        Sets method-level configuration for create_a_vehicle.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._create_a_vehicle_config = config
        return self

    def set_retrieve_a_vehicle_config(self, config: SdkConfig):
        """
        Sets method-level configuration for retrieve_a_vehicle.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._retrieve_a_vehicle_config = config
        return self

    def set_update_a_collection_config(self, config: SdkConfig):
        """
        Sets method-level configuration for update_a_collection.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._update_a_collection_config = config
        return self

    def set_delete_a_vehicle_config(self, config: SdkConfig):
        """
        Sets method-level configuration for delete_a_vehicle.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._delete_a_vehicle_config = config
        return self

    def set_get_all_vehicles_config(self, config: SdkConfig):
        """
        Sets method-level configuration for get_all_vehicles.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._get_all_vehicles_config = config
        return self

    @cast_models
    def create_a_vehicle(
        self,
        request_body: CreateAVehicleRequest,
        *,
        request_config: Optional[SdkConfig] = None,
    ) -> Any:
        """create_a_vehicle

        :param request_body: The request body.
        :type request_body: CreateAVehicleRequest
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        Validator(CreateAVehicleRequest).is_nullable().validate(request_body)

        resolved_config = self._get_resolved_config(
            self._create_a_vehicle_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.DEFAULT.url}/vehicles",
                [self.get_api_key(resolved_config)],
                resolved_config,
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response, status, _ = self.send_request(serialized_request)
        return response

    @cast_models
    def retrieve_a_vehicle(
        self, id_: str, *, request_config: Optional[SdkConfig] = None
    ) -> Any:
        """retrieve_a_vehicle

        :param id_: id_
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        Validator(str).validate(id_)

        resolved_config = self._get_resolved_config(
            self._retrieve_a_vehicle_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.DEFAULT.url}/vehicles/{{id}}",
                [self.get_api_key(resolved_config)],
                resolved_config,
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response, status, _ = self.send_request(serialized_request)
        return response

    @cast_models
    def update_a_collection(
        self,
        request_body: CreateAVehicleRequest,
        id_: str,
        *,
        request_config: Optional[SdkConfig] = None,
    ) -> Any:
        """update_a_collection

        :param request_body: The request body.
        :type request_body: CreateAVehicleRequest
        :param id_: id_
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        Validator(CreateAVehicleRequest).is_nullable().validate(request_body)
        Validator(str).validate(id_)

        resolved_config = self._get_resolved_config(
            self._update_a_collection_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.DEFAULT.url}/vehicles/{{id}}",
                [self.get_api_key(resolved_config)],
                resolved_config,
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PATCH")
            .set_body(request_body)
        )

        response, status, _ = self.send_request(serialized_request)
        return response

    @cast_models
    def delete_a_vehicle(
        self, id_: str, *, request_config: Optional[SdkConfig] = None
    ) -> str:
        """delete_a_vehicle

        :param id_: id_
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: str
        """

        Validator(str).validate(id_)

        resolved_config = self._get_resolved_config(
            self._delete_a_vehicle_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.DEFAULT.url}/vehicles/{{id}}",
                [self.get_api_key(resolved_config)],
                resolved_config,
            )
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response, status, _ = self.send_request(serialized_request)
        return response

    @cast_models
    def get_all_vehicles(self, *, request_config: Optional[SdkConfig] = None) -> Any:
        """get_all_vehicles

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Any
        """

        resolved_config = self._get_resolved_config(
            self._get_all_vehicles_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.DEFAULT.url}/vehicles",
                [self.get_api_key(resolved_config)],
                resolved_config,
            )
            .serialize()
            .set_method("GET")
        )

        response, status, _ = self.send_request(serialized_request)
        return response
