# VehicleServiceCollectionSdk Python SDK 1.0.0

Welcome to the VehicleServiceCollectionSdk SDK documentation. This guide will help you get started with integrating and using the VehicleServiceCollectionSdk SDK in your project.

## Versions

- SDK version: `1.0.0`

## About the API

My spec

## Table of Contents

- [Setup & Configuration](#setup--configuration)
  - [Supported Language Versions](#supported-language-versions)
  - [Installation](#installation)
- [Authentication](#authentication)
  - [API Key Authentication](#api-key-authentication)
- [Setting a Custom Timeout](#setting-a-custom-timeout)
- [Sample Usage](#sample-usage)
- [Async Usage](#async-usage)
- [Services](#services)
- [Models](#models)

# Setup & Configuration

## Supported Language Versions

This SDK is compatible with the following versions: `Python >= 3.9`

## Installation

To get started with the SDK, we recommend installing using `pip`:

```bash
pip install vehicle_service_collection_sdk
```

If you are using Python 3, you can use `pip3` instead:

```bash
pip3 install vehicle_service_collection_sdk
```

## Authentication

### API Key Authentication

The VehicleServiceCollectionSdk API uses API keys as a form of authentication. An API key is a unique identifier used to authenticate a user, developer, or a program that is calling the API.

#### Setting the API key

When you initialize the SDK, you can set the API key as follows:

```py
VehicleServiceCollectionSdk(
    api_key="YOUR_API_KEY",
    timeout=10
)
```

If you need to set or update the API key after initializing the SDK, you can use:

```py
sdk.set_api_key("YOUR_API_KEY")
```

## Setting a Custom Timeout

You can set a custom timeout for the SDK's HTTP requests as follows:

```py
from vehicle_service_collection_sdk import VehicleServiceCollectionSdk

sdk = VehicleServiceCollectionSdk(timeout=10)
```

# Sample Usage

Below is a comprehensive example demonstrating how to authenticate and call a simple endpoint:

```py
from vehicle_service_collection_sdk import VehicleServiceCollectionSdk, Environment

sdk = VehicleServiceCollectionSdk(
    api_key="YOUR_API_KEY",
    base_url=Environment.DEFAULT.value,
    timeout=10
)

result = sdk.vehicle_service_collection_sdk.get_all_vehicles()

print(result)

```

# Async Usage

The SDK includes an Async Client for making asynchronous API requests. This is useful for applications that need non-blocking operations, like web servers or apps with a graphical user interface.

```py
import asyncio
from vehicle_service_collection_sdk import VehicleServiceCollectionSdkAsync, Environment
from vehicle_service_collection_sdk.models import CreateAVehicleRequest

sdk = VehicleServiceCollectionSdkAsync(
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

async def main():
  result = await sdk.vehicle_service_collection_sdk.create_a_vehicle(request_body=request_body)
  print(result)

asyncio.run(main())
```

## Services

The SDK provides various services to interact with the API.

<details>
<summary>Below is a list of all available services with links to their detailed documentation:</summary>

| Name                                                                                               |
| :------------------------------------------------------------------------------------------------- |
| [VehicleServiceCollectionSdkService](documentation/services/VehicleServiceCollectionSdkService.md) |

</details>

## Models

The SDK includes several models that represent the data structures used in API requests and responses. These models help in organizing and managing the data efficiently.

<details>
<summary>Below is a list of all available models with links to their detailed documentation:</summary>

| Name                                                                   | Description |
| :--------------------------------------------------------------------- | :---------- |
| [CreateAVehicleRequest](documentation/models/CreateAVehicleRequest.md) |             |

</details>
