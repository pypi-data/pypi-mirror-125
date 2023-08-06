import json

from functools import cache
from contextlib import suppress
from typing import Union, Any



class LazyJSON:
    """A wrapper for a JSON object
    that only loads entries on request

    OBS! This is meant as read-only
    """

    data: Union[list, dict]

    def __init__(self, data: Union[list, dict]):
        self.data = data

    def __str__(self):
        return str(self.data)

    @cache
    def __getitem__(self, key: Union[int, str]):
        return loads(self.data[key])


    def get(self, key: Union[int, str], default: Any = None):
        if isinstance(key, int):
            with suppress(IndexError):
                return self[key]

        if isinstance(key, str):
            with suppress(KeyError):
                return self[key]

        return default


def loads(data: Union[None, bool, int, str, list, dict]):
    # Lists and dictionaries can be used for `LazyJSON`
    if isinstance(data, (list, dict)):
        return LazyJSON(data)

    # Attempt to load strings as JSON
    if isinstance(data, str):
        try:
            data = loads(json.loads(data))
            return data
        except json.JSONDecodeError:
            return data

    # Return all other data types as is
    return data