"""
cobra.access

Runtime access validation engine.

All decorators and descriptors delegate their access
checks to this module.
"""

from inspect import currentframe

from .enums import AccessType, Operation
from .policy import POLICIES

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

    v0.2.1 
    Updated it to policy for better use.
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

    
        if caller_self is None:
            return False
        # Updated to policy 
        policy = POLICIES[access]
        return policy.check(
                owner=owner,
                caller=caller_self,
                member=member,
                operation=operation,
            )

        raise NotImplementedError(
            f"{access.name} access has not been implemented."
        )

    finally:
        del frame