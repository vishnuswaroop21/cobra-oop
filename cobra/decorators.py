"""
cobra.decorators

Decorators for enforcing optional OOP access modifiers.

Version: 0.1.0
"""

from functools import wraps

from .exceptions import PrivateAccessError
from .utils import is_private_access_allowed


def private(func):
    """
    Marks a method as private.

    A private method may only be called from within
    the declaring class.

    Example:
        class Person:

            @private
            def secret(self):
                ...
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_private_access_allowed(func, args):
            raise PrivateAccessError(
                f"Private method '{func.__qualname__}' cannot be accessed from outside its class."
            )

        return func(*args, **kwargs)

    return wrapper


def protected(func):
    raise NotImplementedError(
        "@protected will be implemented in COBRA v0.2"
    )


def public(func):
    return func


def final(func):
    raise NotImplementedError(
        "@final will be implemented in COBRA v0.2"
    )


def override(func):
    raise NotImplementedError(
        "@override will be implemented in COBRA v0.2"
    )