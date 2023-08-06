from typing import Callable
from px_client_builder import Client as BaseClient

from ..query import QueryExecutor
from ..const import API_URL
from .utils import default_response_resolver

from .geography import GeographyClient


__all__ = 'Client',


class Client(BaseClient):
    query: QueryExecutor

    geo: GeographyClient = GeographyClient.as_property()

    def __init__(
        self,
        *_,
        key: str,
        url: str = API_URL,
        format: str = 'json',
        response_resolver: Callable = default_response_resolver,
        **kw,
    ) -> None:
        super().__init__(**kw)

        self.response_resolver = response_resolver
        self.query = QueryExecutor(key, url=url, format=format)
