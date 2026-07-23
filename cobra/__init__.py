"""
COBRA

Comprehensive Object-Based Runtime Architecture

Runtime-enforced object-oriented access control for Python.
"""

from .base import CobraObject
from .decorators import (
    private,
    protected,
    public,
    final,
    override,
)
from .fields import (
    PrivateField,
    ProtectedField,
)
from .runtime import CobraRuntime
from .exceptions import (
    CobraError,
    PrivateAccessError,
    ProtectedAccessError,
    FinalClassError,
    FinalOverrideError,
    FinalMethodError,
    OverrideError,
)

__version__ = "0.4.0"

__all__ = [
    # Base
    "CobraObject",

    # Decorators
    "private",
    "protected",
    "public",
    "final",
    "override",

    # Fields
    "PrivateField",
    "ProtectedField",

    # Runtime
    "CobraRuntime",

    # Exceptions
    "CobraError",
    "PrivateAccessError",
    "ProtectedAccessError",
    "FinalClassError",
    "FinalOverrideError",
    "FinalMethodError",
    "OverrideError",
]
