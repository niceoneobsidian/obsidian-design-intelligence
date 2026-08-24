"""Generic deterministic registry primitive."""
from typing import Generic, TypeVar

T = TypeVar("T")

class Registry(Generic[T]):
    def __init__(self) -> None:
        self._items: dict[str, T] = {}

    def register(self, item_id: str, item: T) -> T:
        if item_id in self._items:
            raise ValueError(f"Already registered: {item_id}")
        self._items[item_id] = item
        return item

    def upsert(self, item_id: str, item: T) -> T:
        self._items[item_id] = item
        return item

    def get(self, item_id: str) -> T:
        return self._items[item_id]

    def maybe_get(self, item_id: str) -> T | None:
        return self._items.get(item_id)

    def list(self) -> tuple[T, ...]:
        return tuple(self._items.values())

    def contains(self, item_id: str) -> bool:
        return item_id in self._items

    def remove(self, item_id: str) -> T:
        return self._items.pop(item_id)
