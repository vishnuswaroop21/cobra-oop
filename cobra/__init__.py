"""
COBRA
=====

Comprehensive Object-Based Runtime Architecture

Optional runtime-enforced OOP features for Python.

Author: Vishnu Swaroop
Version: 0.2.0
"""

from .base import CobraObject
from .decorators import (
    private,
    protected,
    public,
    final,
    override,
)
from .exceptions import (
    CobraError,
    PrivateAccessError,
    ProtectedAccessError,
    FinalMethodError,
    OverrideError,
    CobraConfigurationError,
)
from .fields import (
    PrivateField,
    ProtectedField,
)

__version__ = "0.2.0"

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

    # Exceptions
    "CobraError",
    "PrivateAccessError",
    "ProtectedAccessError",
    "FinalMethodError",
    "OverrideError",
    "CobraConfigurationError",
]
