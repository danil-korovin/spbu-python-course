from collections.abc import MutableMapping
from typing import Any, List, Tuple, Iterator


class HashTable(MutableMapping):
    """
    Hash table with chains to resolve collisions.

    Attributes:
        size(int): Number of items in hash table.
        num_slots(int): Number of slots.
        hash_table(List[List[Tuple[Any, Any]]]): Hash table.
    """

    def __init__(self, num_slots: int = 8):
        """
        Initialization of hash table.

        Args:
            num_slots(int): Number of slots in hash table.
        """
        self.size = 0
        self.num_slots = num_slots
        self.hash_table: List[List[Tuple[Any, Any]]] = [
            [] for _ in range(self.num_slots)
        ]

    def _hash(self, key: Any) -> int:
        """
        Find hash index.

        Args:
            key(Any): The key for hash.

        Return:
            int: Index in hash table.
        """
        return hash(key) % self.num_slots

    def _resize(self, new_num_slots: int) -> None:
        """
        Resize hash table with new number of slots.

        Args:
            new_num_slots(int): New number of slots.
        """
        old_hash_table = self.hash_table
        self.num_slots = new_num_slots
        self.hash_table = [[] for _ in range(self.num_slots)]
        self.size = 0
        for slot in old_hash_table:
            for k, v in slot:
                self[k] = v

    def __getitem__(self, key: Any) -> Any:
        """
        Get the value.

        Args:
            key(Any): Key.

        Return:
            Any: Value.

        Raise:
            KeyError: If key not found.
        """
        ind = self._hash(key)
        slot = self.hash_table[ind]
        for k, v in slot:
            if k == key:
                return v
        raise KeyError(key)

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Insert or update item.

        Args:
            key(Any): Key.
            value(Any): Value.
        """
        if self.size + 1 > self.num_slots * 0.8:
            self._resize(self.num_slots * 2)

        ind = self._hash(key)
        slot = self.hash_table[ind]
        fl = False
        for item in slot:
            if item[0] == key:
                slot[slot.index(item)] = (key, value)
                fl = True
                break
        if not fl:
            slot.append((key, value))
            self.size += 1

    def __delitem__(self, key: Any) -> None:
        """
        Remove item.

        Args:
            key(Any): Key.

        Raise:
            KeyError: If key not found.
        """
        ind = self._hash(key)
        slot = self.hash_table[ind]
        for k, v in slot:
            if k == key:
                slot.remove((k, v))
                self.size -= 1
                return
        raise KeyError(key)

    def __iter__(self) -> Iterator:
        """
        Iterate all keys.

        Return:
            Iterator: Keys.
        """
        for slot in self.hash_table:
            for k, _ in slot:
                yield k

    def __len__(self) -> int:
        """
        Get the number of items.

        Return:
            int: Number of items.
        """
        return self.size

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
        for k, _ in slot:
            if k == key:
                return True
        return False

    def clear(self):
        """Remove all items."""
        self.hash_table = [[] for _ in range(self.num_slots)]
        self.size = 0
