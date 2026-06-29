"""
cobra.exceptions

Custom exceptions used throughout the COBRA framework.
"""


class CobraError(Exception):
    """
    Base exception for all COBRA-related errors.
    """

    pass


class PrivateAccessError(CobraError):
    """
    Raised when a private method is accessed
    from outside its declaring class.
    """

    pass


class ProtectedAccessError(CobraError):
    """
    Raised when a protected member is accessed
    from an unauthorized context.

    (Reserved for COBRA v0.2)
    """

    pass


class FinalMethodError(CobraError):
    """
    Raised when attempting to override
    a final method.

    (Reserved for COBRA v0.2)
    """

    pass


class OverrideError(CobraError):
    """
    Raised when an @override method does not
    override any method in the parent class.

    (Reserved for COBRA v0.2)
    """

    pass


class CobraConfigurationError(CobraError):
    """
    Raised when COBRA is used incorrectly,
    such as applying decorators to unsupported
    objects.
    """

    pass