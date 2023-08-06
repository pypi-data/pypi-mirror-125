from requests import request, Response

from .const import API_URL


__all__ = 'QueryExecutor',


class QueryExecutor:
    def __init__(
        self,
        url: str = API_URL,
    ) -> None:
        self.url = url

    def make_request(self, url: str, *args, method: str = 'GET', **kwargs):
        kwargs.setdefault('headers', {})

        response = request(method, url, *args, **kwargs)
        response.raise_for_status()
        return response

    def __call__(
        self,
        command: str,
        method: str = 'GET',
        params: dict = {},
        headers: dict = {},
        **kwargs
    ) -> Response:
        return self.make_request(
            self.url.format(command=command),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                **headers,
            },
            params=params,
            method=method,
            **kwargs,
        )
