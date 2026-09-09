from typing import Awaitable, Optional, Any, Union
from .utils.to_async import to_async
from ..vehicle_service_collection_sdk import VehicleServiceCollectionSdkService
from ...net.sdk_config import SdkConfig
from ...models import CreateAVehicleRequest


class VehicleServiceCollectionSdkServiceAsync(VehicleServiceCollectionSdkService):
    """
    Async Wrapper for VehicleServiceCollectionSdkServiceAsync
    """

    def create_a_vehicle(
        self,
        request_body: CreateAVehicleRequest,
        *,
        request_config: Optional[SdkConfig] = None,
    ) -> Awaitable[Any]:
        return to_async(super().create_a_vehicle)(
            request_body, request_config=request_config
        )

    def retrieve_a_vehicle(
        self, id_: str, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[Any]:
        return to_async(super().retrieve_a_vehicle)(id_, request_config=request_config)

    def update_a_collection(
        self,
        request_body: CreateAVehicleRequest,
        id_: str,
        *,
        request_config: Optional[SdkConfig] = None,
    ) -> Awaitable[Any]:
        return to_async(super().update_a_collection)(
            request_body, id_, request_config=request_config
        )

    def delete_a_vehicle(
        self, id_: str, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[str]:
        return to_async(super().delete_a_vehicle)(id_, request_config=request_config)

    def get_all_vehicles(
        self, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[Any]:
        return to_async(super().get_all_vehicles)(request_config=request_config)
