"""
cobra.base

Base object for all COBRA-enabled classes.

Version: 0.2.1
"""

from .runtime import CobraRuntime


class CobraObject:
    """
    Base class for all COBRA objects.

    Provides:

    - Automatic runtime registration
    - Helpful object representation

    Future versions will add:

    - Runtime interception
    - Contract validation
    - Reflection utilities
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        CobraRuntime.register_class(cls)
        CobraRuntime.register_class_friends(cls)

    def __repr__(self):
        return f"<{self.__class__.__name__} at {hex(id(self))}>"

    __str__ = __repr__
