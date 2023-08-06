from functools import cached_property
from typing import Callable


__all__ = 'default_response_resolver', 'query_caller',


def default_response_resolver(response) -> dict:
    return response.json()


def clear_nones(parameters: dict) -> dict:
    return {k: v for k, v in parameters.items() if v is not None}


def query_caller(model: str, method: str) -> Callable:
    def prop(self):
        def caller(**kwargs):
            return self.root.response_resolver(self.root.query(
                model, method, kwargs=clear_nones(kwargs)
            ))

        return caller

    return cached_property(prop)
