"""
cobra.decorators

Runtime access decorators.

COBRA decorators are intentionally lightweight.
All validation is delegated to the runtime access engine.
"""

from functools import wraps

from .access import check_access
from .enums import AccessType, MemberType, Operation
from .exceptions import (
    PrivateAccessError,
    ProtectedAccessError,
)


def private(func):
    """
    Marks a method as private.

    Private methods may only be accessed from within
    the declaring class.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not args:
            raise PrivateAccessError(
                f"Private method '{func.__qualname__}' "
                "must be called on an instance."
            )

        instance = args[0]

        allowed = check_access(
            access=AccessType.PRIVATE,
            member_type=MemberType.METHOD,
            operation=Operation.CALL,
            owner=instance.__class__,
            instance=instance,
            member=func.__name__,
        )

        if not allowed:
            raise PrivateAccessError(
                f"Private method "
                f"'{func.__qualname__}' "
                "cannot be accessed from outside its class."
            )

        return func(*args, **kwargs)

    return wrapper


def protected(func):
    """
    Marks a method as protected.

    Protected methods may only be accessed
    from within the declaring class and subclasses.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not args:
            raise ProtectedAccessError(
                f"Protected method '{func.__qualname__}' "
                "must be called on an instance."
            )

        instance = args[0]

        allowed = check_access(
            access=AccessType.PROTECTED,
            member_type=MemberType.METHOD,
            operation=Operation.CALL,
            owner=instance.__class__,
            instance=instance,
            member=func.__name__,
        )

        if not allowed:
            raise ProtectedAccessError(
                f"Protected method "
                f"'{func.__qualname__}' "
                "cannot be accessed from outside its class hierarchy."
            )

        return func(*args, **kwargs)

    return wrapper


def public(func):
    """
    Public methods require no runtime checks.
    """
    return func


def final(func):
    """
    Placeholder for COBRA v0.4.
    """
    raise NotImplementedError(
        "@final will be implemented in COBRA v0.4"
    )


def override(func):
    """
    Placeholder for COBRA v0.4.
    """
    raise NotImplementedError(
        "@override will be implemented in COBRA v0.4"
    )