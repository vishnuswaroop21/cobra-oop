"""
cobra.access

Runtime access validation engine.

All decorators and descriptors delegate their access
checks to this module.
"""

from inspect import currentframe

from .enums import AccessType, Operation


def check_access(
    *,
    access: AccessType,
    member_type,
    operation: Operation,
    owner: type,
    instance,
    member: str,
) -> bool:
    """
    Determines whether the current caller is permitted
    to access a COBRA member.
    """

    frame = currentframe()

    try:
        #
        # Expected stack (v0.2)
        #
        # User Code
        #     ↓
        # Decorator Wrapper / Descriptor (__get__/__set__)
        #     ↓
        # check_access()
        #

        access_frame = frame.f_back

        if access_frame is None:
            return False

        caller_frame = access_frame.f_back

        if caller_frame is None:
            return False

        caller_self = caller_frame.f_locals.get("self")

        #
        # External code (module/function)
        #
        if caller_self is None:
            return False

        #
        # Public members
        #
        if access is AccessType.PUBLIC:
            return True

        #
        # Private members
        #
        if access is AccessType.PRIVATE:
            return isinstance(caller_self, owner)

        #
        # Protected members
        #
        if access is AccessType.PROTECTED:
            return issubclass(caller_self.__class__, owner)

        raise NotImplementedError(
            f"{access.name} access has not been implemented."
        )

    finally:
        del frame