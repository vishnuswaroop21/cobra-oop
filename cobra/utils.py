"""
cobra.utils

Utility functions used by COBRA decorators.
"""

import inspect


def is_private_access_allowed(func, args):
    """
    Returns True if a private method is being called
    from within its declaring class.

    NOTE:
    This is a Proof-of-Concept implementation for COBRA v0.1.
    It is not intended to be security hardened.
    """

    # Private methods should always be instance methods.
    if not args:
        return False

    instance = args[0]
    owner_class = instance.__class__

    # The caller is two frames above:
    #
    # user_code()
    #   -> wrapper()
    #       -> is_private_access_allowed()
    #
    frame = inspect.currentframe()

    try:
        wrapper_frame = frame.f_back
        caller_frame = wrapper_frame.f_back

        if caller_frame is None:
            return False

        caller_self = caller_frame.f_locals.get("self")

        # No 'self' means the caller is outside any instance method.
        if caller_self is None:
            return False

        # Allow calls only from the same instance type.
        return isinstance(caller_self, owner_class)

    finally:
        # Prevent reference cycles.
        del frame