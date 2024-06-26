import httpx

from .authentication import AuthenticationStrategy
from .evaluation import Evaluation
from .flags import SyncFlag


class FliptClient:
    def __init__(
        self,
        url: str = "http://localhost:8080",
        headers: dict[str, str] | None = None,
        timeout: int = 60,
        authentication: AuthenticationStrategy | None = None,
    ):
        self.httpx_client = httpx.Client(timeout=timeout)

        self.evaluation = Evaluation(url, headers, authentication, self.httpx_client)
        self.flag = SyncFlag(url, headers, authentication, self.httpx_client)

    def close(self) -> None:
        self.httpx_client.close()
