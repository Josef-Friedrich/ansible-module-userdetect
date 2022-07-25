"""
This type stub file was generated by pyright.
"""

from ansible.module_utils.common._collections_compat import Hashable, Mapping

"""Collection of low-level utility functions."""
__metaclass__ = type

class ImmutableDict(Hashable, Mapping):
    """Dictionary that cannot be updated"""

    def __init__(self, *args, **kwargs) -> None: ...
    def __getitem__(self, key): ...
    def __iter__(self): ...
    def __len__(self): ...
    def __hash__(self) -> int: ...
    def __eq__(self, other) -> bool: ...
    def __repr__(self): ...
    def union(self, overriding_mapping):  # -> ImmutableDict:
        """
        Create an ImmutableDict as a combination of the original and overriding_mapping

        :arg overriding_mapping: A Mapping of replacement and additional items
        :return: A copy of the ImmutableDict with key-value pairs from the overriding_mapping added

        If any of the keys in overriding_mapping are already present in the original ImmutableDict,
        the overriding_mapping item replaces the one in the original ImmutableDict.
        """
        ...
    def difference(self, subtractive_iterable):  # -> ImmutableDict:
        """
        Create an ImmutableDict as a combination of the original minus keys in subtractive_iterable

        :arg subtractive_iterable: Any iterable containing keys that should not be present in the
            new ImmutableDict
        :return: A copy of the ImmutableDict with keys from the subtractive_iterable removed
        """
        ...

def is_string(seq):  # -> Any | bool:
    """Identify whether the input has a string-like type (inclding bytes)."""
    ...

def is_iterable(seq, include_strings=...):  # -> bool:
    """Identify whether the input is an iterable."""
    ...

def is_sequence(seq, include_strings=...):  # -> bool:
    """Identify whether the input is a sequence.

    Strings and bytes are not sequences here,
    unless ``include_string`` is ``True``.

    Non-indexable things are never of a sequence type.
    """
    ...

def count(seq):  # -> dict[Unknown, Unknown]:
    """Returns a dictionary with the number of appearances of each element of the iterable.

    Resembles the collections.Counter class functionality. It is meant to be used when the
    code is run on Python 2.6.* where collections.Counter is not available. It should be
    deprecated and replaced when support for Python < 2.7 is dropped.
    """
    ...
