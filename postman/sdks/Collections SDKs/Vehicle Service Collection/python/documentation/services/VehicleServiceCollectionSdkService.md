# VehicleServiceCollectionSdkService

A list of all methods in the `VehicleServiceCollectionSdkService` service. Click on the method name to view detailed information about that method.

| Methods                                     | Description |
| :------------------------------------------ | :---------- |
| [create_a_vehicle](#create_a_vehicle)       |             |
| [retrieve_a_vehicle](#retrieve_a_vehicle)   |             |
| [update_a_collection](#update_a_collection) |             |
| [delete_a_vehicle](#delete_a_vehicle)       |             |
| [get_all_vehicles](#get_all_vehicles)       |             |

## create_a_vehicle

- HTTP Method: `POST`
- Endpoint: `/vehicles`

**Parameters**

| Name         | Type                                                        | Required | Description       |
| :----------- | :---------------------------------------------------------- | :------- | :---------------- |
| request_body | [CreateAVehicleRequest](../models/CreateAVehicleRequest.md) | ✅       | The request body. |

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from vehicle_service_collection_sdk import VehicleServiceCollectionSdk, Environment
from vehicle_service_collection_sdk.models import CreateAVehicleRequest

sdk = VehicleServiceCollectionSdk(
    api_key="YOUR_API_KEY",
    base_url=Environment.DEFAULT.value,
    timeout=10
)

request_body = CreateAVehicleRequest(
    nick_name="The Lisa Marie",
    vin="4M2DV11W4RDJ53329",
    make="Mercury",
    model="Villager",
    year="1994",
    miles=159864
)

result = sdk.vehicle_service_collection_sdk.create_a_vehicle(request_body=request_body)

print(result)
```

## retrieve_a_vehicle

- HTTP Method: `GET`
- Endpoint: `/vehicles/{id}`

**Parameters**

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| id\_ | str  | ✅       |             |

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from vehicle_service_collection_sdk import VehicleServiceCollectionSdk, Environment

sdk = VehicleServiceCollectionSdk(
    api_key="YOUR_API_KEY",
    base_url=Environment.DEFAULT.value,
    timeout=10
)

result = sdk.vehicle_service_collection_sdk.retrieve_a_vehicle(id_="4")

print(result)
```

## update_a_collection

- HTTP Method: `PATCH`
- Endpoint: `/vehicles/{id}`

**Parameters**

| Name         | Type                                                        | Required | Description       |
| :----------- | :---------------------------------------------------------- | :------- | :---------------- |
| request_body | [CreateAVehicleRequest](../models/CreateAVehicleRequest.md) | ✅       | The request body. |
| id\_         | str                                                         | ✅       |                   |

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from vehicle_service_collection_sdk import VehicleServiceCollectionSdk, Environment
from vehicle_service_collection_sdk.models import CreateAVehicleRequest

sdk = VehicleServiceCollectionSdk(
    api_key="YOUR_API_KEY",
    base_url=Environment.DEFAULT.value,
    timeout=10
)

request_body = CreateAVehicleRequest(
    nick_name="The Lisa Marie",
    vin="4M2DV11W4RDJ53329",
    make="Mercury",
    model="Villager",
    year="1994",
    miles=159864
)

result = sdk.vehicle_service_collection_sdk.update_a_collection(
    request_body=request_body,
    id_="4"
)

print(result)
```

## delete_a_vehicle

- HTTP Method: `DELETE`
- Endpoint: `/vehicles/{id}`

**Parameters**

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| id\_ | str  | ✅       |             |

**Return Type**

`str`

**Example Usage Code Snippet**

```python
from vehicle_service_collection_sdk import VehicleServiceCollectionSdk, Environment

sdk = VehicleServiceCollectionSdk(
    api_key="YOUR_API_KEY",
    base_url=Environment.DEFAULT.value,
    timeout=10
)

result = sdk.vehicle_service_collection_sdk.delete_a_vehicle(id_="4")

with open("output-file.ext", "w") as f:
    f.write(result if isinstance(result, str) else result.decode(errors="replace") if isinstance(result, (bytes, bytearray)) else str(result))
```

## get_all_vehicles

- HTTP Method: `GET`
- Endpoint: `/vehicles`

**Return Type**

`Any`

**Example Usage Code Snippet**

```python
from vehicle_service_collection_sdk import VehicleServiceCollectionSdk, Environment

sdk = VehicleServiceCollectionSdk(
    api_key="YOUR_API_KEY",
    base_url=Environment.DEFAULT.value,
    timeout=10
)

result = sdk.vehicle_service_collection_sdk.get_all_vehicles()

print(result)
```
