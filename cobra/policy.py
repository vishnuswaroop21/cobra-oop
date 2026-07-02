"""
cobra.policy

Access policy implementations.

Each policy is responsible for determining whether
a member access is permitted.

COBRA uses the Strategy Pattern so that decorators,
descriptors, and future language features share the
same runtime access engine.
"""

from abc import ABC, abstractmethod


class AccessPolicy(ABC):
    """
    Base class for all access policies.
    """

    @abstractmethod
    def check(
        self,
        *,
        owner: type,
        caller,
        member: str,
        operation,
    ) -> bool:
        """
        Returns True if access should be allowed.
        """
        raise NotImplementedError


class PublicPolicy(AccessPolicy):
    """
    Public members are always accessible.
    """

    def check(
        self,
        *,
        owner,
        caller,
        member,
        operation,
    ) -> bool:
        return True


class PrivatePolicy(AccessPolicy):
    """
    Private members may only be accessed
    from within the declaring class.
    """

    def check(
        self,
        *,
        owner,
        caller,
        member,
        operation,
    ) -> bool:

        if caller is None:
            return False

        return isinstance(caller, owner)


class ProtectedPolicy(AccessPolicy):
    """
    Protected members may be accessed from
    the declaring class and subclasses.
    """

    def check(
        self,
        *,
        owner,
        caller,
        member,
        operation,
    ) -> bool:

        if caller is None:
            return False

        return issubclass(
            caller.__class__,
            owner,
        )


class FriendPolicy(AccessPolicy):
    """
    Placeholder for future Friend support.

    Planned for COBRA v0.3.
    """

    def check(
        self,
        *,
        owner,
        caller,
        member,
        operation,
    ) -> bool:
        raise NotImplementedError(
            "Friend policy is not implemented yet."
        )