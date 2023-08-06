import contextlib
from typing import Iterator

from . import client as _client
from .errors import ClientNotRegisteredError


@contextlib.contextmanager
def reset_client() -> Iterator[None]:
    """Unregister the current client"""
    client = _client._REGISTERED_CLIENT
    if client is None:
        raise ClientNotRegisteredError()

    try:
        _client._REGISTERED_CLIENT = None
        yield
    finally:
        _client._REGISTERED_CLIENT = client
