# -*- encoding: utf-8 -*-

from typing import Iterator, MutableMapping, Optional, Set, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class StackMutableMapping(MutableMapping[K, V]):

    """
    Class representing a stacked mapping. It exposes the usual MutableMapping
    interface, but contains a "fallback" mapping and expose the union of both.
    """

    _parent: Optional["StackMutableMapping[K, V]"]
    _variables: MutableMapping[K, V]
    _deleted: Set[K]

    def __init__(self, parent: Optional["StackMutableMapping[K, V]"] = None):
        self._parent = parent
        self._variables = {}
        self._deleted = set()

    def __delitem__(self, item: K):
        # Remove the item from the list of variables:
        if item in self._variables:
            del self._variables[item]

        # If item is not in the parent:
        elif self._parent is None or item not in self._parent:
            raise KeyError(item)

        self._deleted.add(item)

    def __setitem__(self, item: K, value: V):
        # Remove the item from the list of deleted item:
        if item in self._deleted:
            self._deleted.remove(item)

        # Set the value:
        self._variables[item] = value

    def __getitem__(self, item: K) -> V:
        # If item in the current list, returns it:
        if item in self._variables:
            return self._variables[item]

        # If item was deleted, throw:
        if item in self._deleted or self._parent is None:
            raise KeyError(item)

        # Fallback to parent:
        return self._parent[item]

    def __iter__(self) -> Iterator[K]:
        # Retrieve the parent keys:
        keys: Set[K] = set()

        if self._parent is not None:
            keys.update(self._parent)
            keys.difference_update(self._deleted)

        keys.update(self._variables)

        return iter(keys)

    def __len__(self) -> int:
        # Retrieve the parent keys:
        keys: Set[K] = set()

        if self._parent is not None:
            keys.update(self._parent)
            keys.difference_update(self._deleted)

        keys.update(self._variables)

        return len(keys)

    def __repr__(self):
        return "StackMutableMapping({})".format({k: self[k] for k in self})
