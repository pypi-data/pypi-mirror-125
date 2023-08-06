from requests import request, Response

from .const import API_URL


__all__ = 'QueryExecutor',


class QueryExecutor:
    def __init__(
        self,
        key: str,
        url: str = API_URL,
        format: str = 'json',
    ) -> None:
        self.key = key
        self.format = format
        self.url = url.format(format=self.format)

    def make_request(self, url: str, *args, method: str = 'POST', **kwargs):
        kwargs.setdefault('headers', {})

        response = request(method, url, *args, **kwargs)
        response.raise_for_status()
        return response

    def __call__(self, model: str, method: str, kwargs: dict = {}) -> Response:
        return self.make_request(
            self.url,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            json={
                'modelName': model,
                'calledMethod': method,
                'methodProperties': kwargs,
                'apiKey': self.key
            },
            method='POST',
        )
