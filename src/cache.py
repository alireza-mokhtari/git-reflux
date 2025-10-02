from __future__ import annotations

from collections import OrderedDict
from typing import Optional


class LRUCache:
    def __init__(self, capacity: int = 256) -> None:
        self.capacity = capacity
        self._data: OrderedDict[str, object] = OrderedDict()

    def get(self, key: str) -> Optional[object]:
        value = self._data.get(key)
        if value is not None:
            self._data.move_to_end(key)
        return value

    def set(self, key: str, value: object) -> None:
        self._data[key] = value
        self._data.move_to_end(key)
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)


