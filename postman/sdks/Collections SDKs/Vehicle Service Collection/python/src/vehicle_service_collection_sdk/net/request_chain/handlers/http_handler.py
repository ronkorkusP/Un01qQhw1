import requests

from requests.exceptions import Timeout
from typing import Generator, Optional, Tuple
from pydantic import TypeAdapter
from .base_handler import BaseHandler
from ...transport.request import Request
from ...transport.response import Response
from ...transport.api_error import ApiError


class HttpHandler(BaseHandler):
    """
    Handler for making HTTP requests.
    This handler sends the request to the specified URL and returns the response.

    :ivar int _timeout_in_seconds: The timeout for the HTTP request in seconds.
    """

    def __init__(self, timeout=60):
        """
        Initialize a new instance of HttpHandler.
        """
        super().__init__()
        self._timeout_in_seconds = timeout

    def handle(
        self, request: Request
    ) -> Tuple[Optional[Response], Optional[Exception]]:
        """
        Send the request to the specified URL and return the response.

        :param Request request: The request to send.
        :return: The response and any error that occurred.
        :rtype: Tuple[Optional[Response], Optional[Exception]]
        """
        try:
            request_args = self._get_request_data(request)

            # Get timeout from config if available, otherwise use default
            timeout = self._get_timeout_from_config(request)

            result = requests.request(
                request.method,
                request.url,
                headers=request.headers,
                timeout=timeout,
                **request_args,
            )
            response = Response(result)

            if response.status >= 400:
                if response.status in request.errors and isinstance(
                    response.body, dict
                ):
                    error_model_class = request.errors[response.status]
                    if isinstance(error_model_class, TypeAdapter):
                        # TypeAdapter for anyOf/oneOf union type errors: parse into the correct variant
                        try:
                            parsed_body = error_model_class.validate_python(
                                response.body
                            )
                        except Exception:
                            parsed_body = response.body
                        message = response.body.get("message")
                        if not isinstance(message, str):
                            message = (
                                f"{response.status} error in request to: {request.url}"
                            )
                        error = ApiError(
                            message=message,
                            status=response.status,
                            response=response,
                        )
                        error.body = parsed_body
                        return None, error
                    error = error_model_class(**response.body)
                    if "message" not in response.body:
                        error.message = (
                            f"{response.status} error in request to: {request.url}"
                        )
                    error.status = response.status
                    error.response = response

                    return None, error

                return None, ApiError(
                    message=f"{response.status} error in request to: {request.url}",
                    status=response.status,
                    response=response,
                )

            return response, None
        except Timeout:
            return None, ApiError("Request timed out", status=408)

    def stream(
        self, request: Request
    ) -> Generator[Tuple[Optional[Response], Optional[Exception]], None, None]:
        """
        Stream the request to the specified URL and yield response chunks.
        Useful for handling large responses or server-sent events.

        :param request: The request to stream.
        :return: A generator yielding response chunks and any errors that occurred.
        """
        try:
            request_args = self._get_request_data(request)

            # Get timeout from config if available, otherwise use default
            timeout = self._get_timeout_from_config(request)

            result = requests.request(
                request.method,
                request.url,
                headers=request.headers,
                timeout=timeout,
                stream=True,
                **request_args,
            )

            if result.status_code >= 400:
                response = Response(result)
                yield (
                    None,
                    ApiError(
                        message=f"{response.status} error in request to: {request.url}",
                        status=response.status,
                        response=response,
                    ),
                )

            else:
                for chunk in result.iter_content(chunk_size=8192):
                    for response in Response.from_chunk(result, chunk):
                        yield response, None

        except Timeout:
            yield None, ApiError("Request timed out", status=408)

    def _get_request_data(self, request: Request) -> dict:
        """
        Get the request arguments based on the request headers and data.

        :param Request request: The request object.
        :return: The request arguments.
        :rtype: dict
        """
        headers = request.headers or {}

        # No body was set on the request (the operation declares no requestBody).
        # Sending an empty JSON payload would force a Content-Type the endpoint
        # never advertises, which strict servers reject with HTTP 415.
        if request.body is None:
            return {}

        data = request.body or {}
        content_type = headers.get("Content-Type", "application/json")

        if request.method == "GET" and not data:
            return {}

        # Raw binary bodies (e.g. application/octet-stream, file uploads) must be
        # sent as-is. Routing them through `json=` crashes with
        # "TypeError: Object of type bytes is not JSON serializable", regardless
        # of what Content-Type the request defaulted to.
        if isinstance(data, (bytes, bytearray)):
            return {"data": data}

        if content_type.startswith("application/") and "json" in content_type:
            return {"json": data}

        if "multipart/form-data" in content_type:
            headers.pop("Content-Type", None)
            files, form_data = {}, {}
            for key, value in data.items():
                if isinstance(value, bytes):
                    files[key] = (key, value, "application/octet-stream")
                else:
                    form_data[key] = value
            return {"files": files, "data": form_data}

        return {"data": data}

    def _get_timeout_from_config(self, request: Request) -> float:
        """
        Get the timeout for the request from config or use default.

        :param Request request: The request object.
        :return: The timeout in seconds.
        :rtype: float
        """
        if request.config and "timeout" in request.config:
            return request.config["timeout"]
        return self._timeout_in_seconds
