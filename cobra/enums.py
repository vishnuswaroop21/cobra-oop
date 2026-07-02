"""
cobra.enums

Enumerations used by COBRA's access control engine.
"""

from enum import Enum, auto


class AccessType(Enum):
    """
    Defines the access level of a member.
    """

    PUBLIC = auto()
    PROTECTED = auto()
    PRIVATE = auto()
    FRIEND = auto()


class MemberType(Enum):
    """
    Defines the type of member being accessed.
    """

    METHOD = auto()
    FIELD = auto()


class Operation(Enum):
    """
    Defines the operation being performed on a member.
    """

    CALL = auto()
    READ = auto()
    WRITE = auto()
    DELETE = auto()