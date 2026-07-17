"""Hash table implementation using separate chaining and universal hashing."""

from __future__ import annotations

import random
from typing import Generic, Iterator, Optional, TypeVar

K = TypeVar("K", bound=int)
V = TypeVar("V")


class HashTableChaining(Generic[V]):
    """Integer-key hash table with separate chaining and dynamic resizing."""

    _PRIME = 2_147_483_647

    def __init__(self, capacity: int = 11, max_load_factor: float = 0.75, seed: int = 2026) -> None:
        if capacity < 2:
            raise ValueError("capacity must be at least 2")
        if not 0 < max_load_factor < 1:
            raise ValueError("max_load_factor must be between 0 and 1")
        self._capacity = self._next_prime(capacity)
        self._max_load_factor = max_load_factor
        self._buckets: list[list[tuple[int, V]]] = [[] for _ in range(self._capacity)]
        self._size = 0
        self._rng = random.Random(seed)
        self._choose_hash_parameters()

    def _choose_hash_parameters(self) -> None:
        self._a = self._rng.randint(1, self._PRIME - 1)
        self._b = self._rng.randint(0, self._PRIME - 1)

    def _hash(self, key: int) -> int:
        if not isinstance(key, int):
            raise TypeError("This implementation requires integer keys")
        return ((self._a * key + self._b) % self._PRIME) % self._capacity

    @property
    def size(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def load_factor(self) -> float:
        return self._size / self._capacity

    def insert(self, key: int, value: V) -> None:
        index = self._hash(key)
        bucket = self._buckets[index]
        for position, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[position] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self.load_factor > self._max_load_factor:
            self._resize(self._next_prime(self._capacity * 2))

    def search(self, key: int) -> Optional[V]:
        index = self._hash(key)
        for existing_key, value in self._buckets[index]:
            if existing_key == key:
                return value
        return None

    def delete(self, key: int) -> bool:
        index = self._hash(key)
        bucket = self._buckets[index]
        for position, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[position]
                self._size -= 1
                return True
        return False

    def _resize(self, new_capacity: int) -> None:
        old_items = list(self.items())
        self._capacity = new_capacity
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        self._choose_hash_parameters()
        for key, value in old_items:
            self.insert(key, value)

    def items(self) -> Iterator[tuple[int, V]]:
        for bucket in self._buckets:
            yield from bucket

    @staticmethod
    def _is_prime(number: int) -> bool:
        if number < 2:
            return False
        if number % 2 == 0:
            return number == 2
        divisor = 3
        while divisor * divisor <= number:
            if number % divisor == 0:
                return False
            divisor += 2
        return True

    @classmethod
    def _next_prime(cls, number: int) -> int:
        candidate = max(2, number)
        while not cls._is_prime(candidate):
            candidate += 1
        return candidate

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: int) -> bool:
        return self.search(key) is not None


if __name__ == "__main__":
    table = HashTableChaining[str](capacity=5)
    table.insert(101, "Alice")
    table.insert(202, "Bob")
    table.insert(303, "Carol")
    table.insert(202, "Robert")  # Updates the existing value.

    print("Search 202:", table.search(202))
    print("Delete 101:", table.delete(101))
    print("Search 101:", table.search(101))
    print("Size:", table.size)
    print("Capacity:", table.capacity)
    print("Load factor:", round(table.load_factor, 3))
