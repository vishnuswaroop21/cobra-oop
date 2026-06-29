"""
cobra.fields

Descriptor implementations for COBRA.

Version: 0.1.0

NOTE:
Field-level encapsulation is planned for COBRA v0.2.
This file provides the initial structure only.
"""

from .exceptions import PrivateAccessError, ProtectedAccessError


class PrivateField:
    """
    Descriptor representing a private field.

    Access control will be enforced in COBRA v0.2.
    """

    def __init__(self, default=None):
        self.default = default
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.storage_name = f"__cobra_private_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # TODO:
        # Enforce private access using caller inspection.
        return getattr(instance, self.storage_name, self.default)

    def __set__(self, instance, value):
        # TODO:
        # Enforce private write access.
        setattr(instance, self.storage_name, value)


class ProtectedField:
    """
    Descriptor representing a protected field.

    Access control will be enforced in COBRA v0.2.
    """

    def __init__(self, default=None):
        self.default = default
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.storage_name = f"__cobra_protected_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # TODO:
        # Enforce protected access.
        return getattr(instance, self.storage_name, self.default)

    def __set__(self, instance, value):
        # TODO:
        # Enforce protected write access.
        setattr(instance, self.storage_name, value)