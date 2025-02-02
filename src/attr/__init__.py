# SPDX-License-Identifier: MIT

"""
Classes Without Boilerplate
"""

from functools import partial
from typing import Callable

from . import converters, exceptions, filters, setters, validators
from ._cmp import cmp_using
from ._compat import Protocol
from ._config import get_run_validators, set_run_validators
from ._funcs import asdict, assoc, astuple, evolve, has, resolve_types
from ._make import (
    NOTHING,
    Attribute,
    Factory,
    attrib,
    attrs,
    fields,
    fields_dict,
    make_class,
    validate,
)
from ._next_gen import define, field, frozen, mutable
from ._version_info import VersionInfo


s = attributes = attrs
ib = attr = attrib
dataclass = partial(attrs, auto_attribs=True)  # happy Easter ;)


class AttrsInstance(Protocol):
    pass


__all__ = [
    "Attribute",
    "AttrsInstance",
    "Factory",
    "NOTHING",
    "asdict",
    "assoc",
    "astuple",
    "attr",
    "attrib",
    "attributes",
    "attrs",
    "cmp_using",
    "converters",
    "define",
    "evolve",
    "exceptions",
    "field",
    "fields",
    "fields_dict",
    "filters",
    "frozen",
    "get_run_validators",
    "has",
    "ib",
    "make_class",
    "mutable",
    "resolve_types",
    "s",
    "set_run_validators",
    "setters",
    "validate",
    "validators",
]


def _make_getattr(mod_name: str) -> Callable:
    """
    Create a metadata proxy for packaging information that uses *mod_name* in
    its warnings and errors.
    """

    def __getattr__(name: str) -> str:
        dunder_to_metadata = {
            "__title__": "Name",
            "__copyright__": "",
            "__version__": "version",
            "__version_info__": "version",
            "__description__": "summary",
            "__uri__": "",
            "__url__": "",
            "__author__": "",
            "__email__": "",
            "__license__": "license",
        }
        if name not in dunder_to_metadata:
            msg = f"module {mod_name} has no attribute {name}"
            raise AttributeError(msg)

        import sys
        import warnings

        from importlib.metadata import metadata

        if name not in ("__version__", "__version_info__"):
            warnings.warn(
                f"Accessing {mod_name}.{name} is deprecated and will be "
                "removed in a future release. Use importlib.metadata directly "
                "to query for attrs's packaging metadata.",
                DeprecationWarning,
                stacklevel=2,
            )

        meta = metadata("attrs")
        if name == "__license__":
            return "MIT"
        if name == "__copyright__":
            return "Copyright (c) 2015 Hynek Schlawack"
        if name in ("__uri__", "__url__"):
            return meta["Project-URL"].split(" ", 1)[-1]
        if name == "__version_info__":
            return VersionInfo._from_version_string(meta["version"])
        if name == "__author__":
            return meta["Author-email"].rsplit(" ", 1)[0]
        if name == "__email__":
            return meta["Author-email"].rsplit("<", 1)[1][:-1]

        return meta[dunder_to_metadata[name]]

    return __getattr__


__getattr__ = _make_getattr(__name__)
