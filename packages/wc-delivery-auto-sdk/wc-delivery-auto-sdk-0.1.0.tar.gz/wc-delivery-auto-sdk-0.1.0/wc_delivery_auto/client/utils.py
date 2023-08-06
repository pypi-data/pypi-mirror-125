from functools import cached_property
from typing import Callable


__all__ = 'default_response_resolver', 'query_caller',


def default_response_resolver(response) -> dict:
    return response.json()


def clear_nones(parameters: dict) -> dict:
    return {k: v for k, v in parameters.items() if v is not None}


def query_caller(command: str, method: str = 'GET') -> Callable:
    def prop(self):
        def caller(params: dict = {}, **kwargs):
            return self.root.response_resolver(self.root.query(
                command=command, method=method, params=clear_nones(params),
                **clear_nones(kwargs)
            ))

        return caller

    return cached_property(prop)
