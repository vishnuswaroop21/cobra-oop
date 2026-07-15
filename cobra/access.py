"""
cobra.access

Runtime access validation engine.

All decorators and descriptors delegate their access
checks to this module.
"""

from inspect import currentframe

from .enums import AccessType
from .runtime import CobraRuntime


def check_access(
    *,
    access,
    member_type,
    operation,
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
        # Expected stack
        #
        # User Code
        #     ↓
        # Decorator / Descriptor
        #     ↓
        # check_access()
        #

        access_frame = frame.f_back

        if access_frame is None:
            return False

        caller_frame = access_frame.f_back

        #
        # Skip CobraObject.__getattribute__()
        #
        while (
            caller_frame
            and caller_frame.f_code.co_name == "__getattribute__"
        ):
            caller_frame = caller_frame.f_back

        if caller_frame is None:
            return False

        caller_self = caller_frame.f_locals.get("self")

        #
        # External function / module
        #
        if caller_self is None:
            return False

        #
        # ----------------------------------------------------------
        # PUBLIC
        # ----------------------------------------------------------
        #
        if access is AccessType.PUBLIC:
            return True

        #
        # ----------------------------------------------------------
        # PRIVATE
        # ----------------------------------------------------------
        #
        if access is AccessType.PRIVATE:

            #
            # Same class
            #
            if isinstance(caller_self, owner):
                return True

            #
            # Friend class
            #
            if CobraRuntime.is_friend(
                owner=owner,
                member=member,
                caller=caller_self,
            ):
                return True

            return False

        #
        # ----------------------------------------------------------
        # PROTECTED
        # ----------------------------------------------------------
        #
        if access is AccessType.PROTECTED:

            #
            # Class hierarchy
            #
            if issubclass(
                caller_self.__class__,
                owner,
            ):
                return True

            #
            # Friend class
            #
            if CobraRuntime.is_friend(
                owner=owner,
                member=member,
                caller=caller_self,
            ):
                return True

            return False

        raise NotImplementedError(
            f"{access.name} access has not been implemented."
        )

    finally:
        del frame