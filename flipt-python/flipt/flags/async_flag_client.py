from http import HTTPStatus

import httpx

from flipt.models import ListParameters

from ..authentication import AuthenticationStrategy
from ..exceptions import FliptApiError
from .models import (
    ListFlagsResponse,
)


class AsyncFlag:
    def __init__(
        self,
        url: str,
        authentication: AuthenticationStrategy | None = None,
        httpx_client: httpx.AsyncClient | None = None,
    ):
        self.url = url
        self.headers: dict[str, str] = {}

        self._client = httpx_client or httpx.AsyncClient()

        if authentication:
            authentication.authenticate(self.headers)

    async def close(self) -> None:
        await self._client.aclose()

    def _raise_on_error(self, response: httpx.Response) -> None:
        if response.status_code != 200:
            body = response.json()
            message = body.get("message", HTTPStatus(response.status_code).description)
            raise FliptApiError(message, response.status_code)

    async def list_flags(self, *, namespace_key: str, params: ListParameters | None = None) -> ListFlagsResponse:
        response = await self._client.get(
            f"{self.url}/api/v1/namespaces/{namespace_key}/flags",
            params=params.model_dump_json(exclude_none=True) if params else {},
            headers=self.headers,
        )
        self._raise_on_error(response)
        return ListFlagsResponse.model_validate_json(response.text)