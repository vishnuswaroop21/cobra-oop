"""
cobra.decorators

Runtime access decorators.

COBRA decorators are intentionally lightweight.
All validation is delegated to the runtime access engine.
"""

from functools import wraps

from .access import check_access
from .enums import (
    AccessType,
    MemberType,
    Operation,
)
from .exceptions import (
    PrivateAccessError,
    ProtectedAccessError,
)


# ------------------------------------------------------------------
# Private
# ------------------------------------------------------------------


def private(func=None, *, friends=None):
    """
    Marks a method as private.

    Supports:

        @private

    and

        @private(friends=[Service])
    """

    friends = frozenset(friends or ())

    def decorator(func):

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

        #
        # Metadata consumed by CobraRuntime during
        # class registration.
        #
        wrapper.__cobra_metadata__ = {
            "access": AccessType.PRIVATE,
            "friends": friends,
        }

        return wrapper

    #
    # Supports:
    #
    # @private
    #
    if callable(func):
        return decorator(func)

    #
    # Supports:
    #
    # @private(friends=[...])
    #
    return decorator


# ------------------------------------------------------------------
# Protected
# ------------------------------------------------------------------


def protected(func=None, *, friends=None):
    """
    Marks a method as protected.

    Supports:

        @protected

    and

        @protected(friends=[Service])
    """

    friends = frozenset(friends or ())

    def decorator(func):

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

        wrapper.__cobra_metadata__ = {
            "access": AccessType.PROTECTED,
            "friends": friends,
        }

        return wrapper

    if callable(func):
        return decorator(func)

    return decorator


# ------------------------------------------------------------------
# Public
# ------------------------------------------------------------------


def public(func):
    """
    Public methods require no runtime checks.
    """
    return func


# ------------------------------------------------------------------
# Placeholders
# ------------------------------------------------------------------


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