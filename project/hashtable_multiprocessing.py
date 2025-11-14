import multiprocessing
from collections.abc import MutableMapping
from typing import Any, Iterator


class HashTable(MutableMapping):
    """
    Hash table with chains to resolve collisions. It supports thread safe using multiprocessing Manager

    Attributes:
        num_slots(int): Number of slots.
        manager(multiprocessing.Manager): Manager object.
        hash_table(multiprocessing.managers.ListProxy): Hash table with slots.
        locks(multiprocessing.managers.ListProxy): List of locks.
    """

    def __init__(self, num_slots: int = 16):
        """
        Initialization of hash table.

        Args:
            num_slots(int): Number of slots in hash table.
        """
        self.num_slots = num_slots
        self.manager = multiprocessing.Manager()
        self.hash_table = self.manager.list(
            [self.manager.list() for i in range(num_slots)]
        )
        self.locks = self.manager.list([self.manager.Lock() for i in range(num_slots)])

    def _hash(self, key: Any) -> int:
        """
        Find hash index.

        Args:
            key(Any): The key for hash.

        Returns:
            int: Index in hash table.
        """
        return hash(key) % self.num_slots

    def __getitem__(self, key: Any) -> Any:
        """
        Get the value.

        Args:
            key(Any): Key.

        Returns:
            Any: Value.

        Raise:
            KeyError: If key not found.
        """
        ind = self._hash(key)
        for k, v in self.hash_table[ind]:
            if k == key:
                return v
        raise KeyError(key)

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Safely insert or update item.

        Args:
            key(Any): Key.
            value(Any): Value.
        """
        ind = self._hash(key)
        with self.locks[ind]:
            slot = self.hash_table[ind]
            for idx, item in enumerate(slot):
                if item[0] == key:
                    slot[idx] = (key, value)
                    return
            slot.append((key, value))

    def __delitem__(self, key: Any) -> None:
        """
        Safely remove item.

        Args:
            key(Any): Key.

        Raise:
            KeyError: If key not found.
        """
        ind = self._hash(key)
        with self.locks[ind]:
            slot = self.hash_table[ind]
            for i, item in enumerate(slot):
                if item[0] == key:
                    del slot[i]
                    return
            raise KeyError(key)

    def __iter__(self) -> Iterator[Any]:
        """
        Safely iterate all keys.

        Returns:
            Iterator: Keys.
        """
        for i in range(self.num_slots):
            with self.locks[i]:
                slot = list(self.hash_table[i])
            for item in slot:
                yield item[0]

    def __len__(self) -> int:
        """
        Safely get the number of items.

        Returns:
            int: Number of items.
        """
        size = 0
        k = self.num_slots
        for i in range(k):
            with self.locks[i]:
                size += len(self.hash_table[i])
        return size

    def __contains__(self, key: Any) -> bool:
        """
        Check if key exist.

        Args:
            key(Any): Key.

        Returns:
            bool: True, if key exist.
        """
        ind = self._hash(key)
        slot = self.hash_table[ind]
        for item in slot:
            if item[0] == key:
                return True
        return False

    def clear(self) -> None:
        """Safely remove all items."""
        k = self.num_slots
        for i in range(k):
            with self.locks[i]:
                self.hash_table[i] = self.manager.list()
