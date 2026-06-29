"""
cobra.object

Base object for all COBRA-enabled classes.

Version: 0.1.0
"""


class CobraObject:
    """
    Base class for all COBRA objects.

    Future versions will provide:

    - Runtime access control
    - Field interception
    - Contract validation
    - Reflection utilities
    - Metadata support
    """

    def __repr__(self):
        return f"<{self.__class__.__name__} at {hex(id(self))}>"

    def __str__(self):
        return self.__repr__()

    # ------------------------------------------------------------------
    # Reserved for COBRA v0.2+
    # ------------------------------------------------------------------

    def __getattribute__(self, name):
        """
        Reserved for future runtime access interception.

        In v0.2 this will become the central point for
        field-level encapsulation.
        """
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        """
        Reserved for future runtime write interception.
        """
        super().__setattr__(name, value)

    def __delattr__(self, name):
        """
        Reserved for future runtime delete interception.
        """
        super().__delattr__(name)