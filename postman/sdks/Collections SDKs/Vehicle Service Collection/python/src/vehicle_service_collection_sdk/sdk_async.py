from typing import Union
from .net.environment import Environment
from .sdk import VehicleServiceCollectionSdk
from .services.async_.vehicle_service_collection_sdk import (
    VehicleServiceCollectionSdkServiceAsync,
)


class VehicleServiceCollectionSdkAsync(VehicleServiceCollectionSdk):
    """
    VehicleServiceCollectionSdkAsync is the asynchronous version of the VehicleServiceCollectionSdk SDK Client.
    """

    def __init__(
        self,
        *,
        api_key: str = None,
        api_key_header: str = "X-API-Key",
        base_url: Union[Environment, str, None] = None,
        timeout: float = None,
        timeout_ms: int = None,
        retry: "RetryConfig" = None,
    ):
        super().__init__(
            api_key=api_key,
            api_key_header=api_key_header,
            base_url=base_url,
            timeout=timeout,
            timeout_ms=timeout_ms,
            retry=retry,
        )

        self.vehicle_service_collection_sdk = VehicleServiceCollectionSdkServiceAsync(
            base_url=self._base_url
        )
        if retry is not None:
            self.set_retry(retry)
