"""
cobra.fields

Descriptor implementations for COBRA.

Version: 0.2.1
"""

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


class PrivateField:
    """
    Descriptor representing a private field.
    """

    def __init__(self, default=None):
        self.default = default
        self.storage_name = None
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = f"__cobra_private_{name}"

    def __get__(self, instance, owner):

        
        if instance is None:
            return self

        allowed = check_access(
            access=AccessType.PRIVATE,
            member_type=MemberType.FIELD,
            operation=Operation.READ,
            owner=owner,
            instance=instance,
            member=self.name,
        )

        if not allowed:
            raise PrivateAccessError(
                f"Private field '{self.name}' cannot be accessed."
            )

        return instance.__dict__.get(
            self.storage_name,
            self.default,
        )

    def __set__(self, instance, value):

        allowed = check_access(
            access=AccessType.PRIVATE,
            member_type=MemberType.FIELD,
            operation=Operation.WRITE,
            owner=instance.__class__,
            instance=instance,
            member=self.name,
        )

        if not allowed:
            raise PrivateAccessError(
                f"Private field '{self.name}' cannot be modified."
            )

        instance.__dict__[self.storage_name] = value


class ProtectedField:
    """
    Descriptor representing a protected field.
    """

    def __init__(self, default=None):
        self.default = default
        self.storage_name = None
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = f"__cobra_protected_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self

        allowed = check_access(
            access=AccessType.PROTECTED,
            member_type=MemberType.FIELD,
            operation=Operation.READ,
            owner=owner,
            instance=instance,
            member=self.name,
        )

        if not allowed:
            raise ProtectedAccessError(
                f"Protected field '{self.name}' cannot be accessed."
            )

        return instance.__dict__.get(
            self.storage_name,
            self.default,
        )

    def __set__(self, instance, value):

        allowed = check_access(
            access=AccessType.PROTECTED,
            member_type=MemberType.FIELD,
            operation=Operation.WRITE,
            owner=instance.__class__,
            instance=instance,
            member=self.name,
        )

        if not allowed:
            raise ProtectedAccessError(
                f"Protected field '{self.name}' cannot be modified."
            )

        instance.__dict__[self.storage_name] = value