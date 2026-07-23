"""
cobra.runtime

COBRA runtime.

Responsible for:

- Class registration
- Runtime configuration
- Friend registration
- Future plugin management
"""

from threading import RLock

from .exceptions import (
    FinalClassError,
    FinalOverrideError,
    OverrideError,
)


class CobraRuntime:
    """
    Global COBRA runtime.

    A singleton-style runtime used by the access engine.
    """

    _lock = RLock()

    _classes = {}

    #
    # owner_class -> member_name -> metadata
    #
    _metadata_registry = {}

    #
    # owner_class -> member_name -> frozenset(friend_classes)
    #
    _friend_registry = {}

    _config = {
        "enabled": True,
        "strict": True,
        "debug": False,
    }

    # ------------------------------------------------------------------
    # Class Registration
    # ------------------------------------------------------------------

    @classmethod
    def register_class(cls, target):
        """
        Registers a CobraObject subclass.
        """

        with cls._lock:
            key = f"{target.__module__}.{target.__qualname__}"
            cls._classes[key] = target

    @classmethod
    def register_class_metadata(cls, target):
        """
        Registers COBRA metadata declared on class members.
        """

        with cls._lock:

            members = cls._metadata_registry.setdefault(
                target,
                {},
            )

            for member_name, member in vars(target).items():

                if not callable(member):
                    continue

                metadata = getattr(
                    member,
                    "__cobra_metadata__",
                    None,
                )

                if metadata is None:
                    continue

                members[member_name] = dict(metadata)

    @classmethod
    def validate_inheritance(cls, target):
        """
        Validates COBRA inheritance rules.
        """

        cls._validate_final_classes(target)
        cls._validate_final_methods(target)
        cls._validate_overrides(target)

    @classmethod
    def _validate_final_classes(cls, target):
        """
        Raises if target inherits from a final class.
        """

        for base in target.__mro__[1:]:

            metadata = getattr(
                base,
                "__cobra_metadata__",
                {},
            )

            if metadata.get("final"):
                raise FinalClassError(
                    f"Final class '{base.__qualname__}' "
                    f"cannot be inherited by '{target.__qualname__}'."
                )

    @classmethod
    def _validate_final_methods(cls, target):
        """
        Raises if target overrides a final method.
        """

        declared_members = vars(target)

        for base in target.__mro__[1:]:

            for member_name, member in vars(base).items():

                if member_name not in declared_members:
                    continue

                if not callable(member):
                    continue

                metadata = getattr(
                    member,
                    "__cobra_metadata__",
                    {},
                )

                if metadata.get("final"):
                    raise FinalOverrideError(
                        f"Final method '{base.__qualname__}."
                        f"{member_name}' cannot be overridden by "
                        f"'{target.__qualname__}.{member_name}'."
                    )

    @classmethod
    def _validate_overrides(cls, target):
        """
        Raises if an @override method does not override a base member.
        """

        for member_name, member in vars(target).items():

            if not callable(member):
                continue

            metadata = getattr(
                member,
                "__cobra_metadata__",
                {},
            )

            if not metadata.get("override"):
                continue

            if any(
                hasattr(base, member_name)
                for base in target.__mro__[1:]
            ):
                continue

            raise OverrideError(
                f"Method '{target.__qualname__}.{member_name}' "
                "is marked @override but does not override "
                "a superclass member."
            )

    @classmethod
    def register_class_friends(cls, target):
        """
        Registers friend metadata declared on COBRA members.
        """

        for member_name, member in vars(target).items():

            if not callable(member):
                continue

            metadata = getattr(
                member,
                "__cobra_metadata__",
                None,
            )

            if metadata is None:
                continue

            friends = metadata.get(
                "friends",
                frozenset(),
            )

            if not friends:
                continue

            cls.register_friend(
                owner=target,
                member=member_name,
                friends=friends,
            )

    @classmethod
    def get_class(cls, qualified_name):
        """
        Returns a registered class.
        """

        return cls._classes.get(qualified_name)

    @classmethod
    def registered_classes(cls):
        """
        Returns all registered classes.
        """

        return dict(cls._classes)

    # ------------------------------------------------------------------
    # Friend Registration
    # ------------------------------------------------------------------

    @classmethod
    def register_friend(
        cls,
        *,
        owner: type,
        member: str,
        friends,
    ):
        """
        Registers friend classes for a member.
        """

        with cls._lock:

            members = cls._friend_registry.setdefault(
                owner,
                {}
            )

            members[member] = frozenset(friends)

    @classmethod
    def get_friends(
        cls,
        *,
        owner: type,
        member: str,
    ):
        """
        Returns all friend classes for a member.
        """

        return (
            cls._friend_registry
            .get(owner, {})
            .get(member, frozenset())
        )

    @classmethod
    def is_friend(
        cls,
        *,
        owner: type,
        member: str,
        caller,
    ):
        """
        Returns True if the caller is a registered friend.
        """

        friends = cls.get_friends(
            owner=owner,
            member=member,
        )

        return isinstance(caller, tuple(friends))

    @classmethod
    def registered_friends(cls):
        """
        Returns a copy of the friend registry.
        """

        return {
            owner: dict(members)
            for owner, members in cls._friend_registry.items()
        }

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    @classmethod
    def configure(cls, **kwargs):
        """
        Updates runtime configuration.
        """

        with cls._lock:
            cls._config.update(kwargs)

    @classmethod
    def config(cls):
        """
        Returns runtime configuration.
        """

        return dict(cls._config)

    @classmethod
    def enable(cls):
        cls._config["enabled"] = True

    @classmethod
    def disable(cls):
        cls._config["enabled"] = False

    @classmethod
    def enabled(cls):
        return cls._config["enabled"]

    # ------------------------------------------------------------------
    # Testing
    # ------------------------------------------------------------------

    @classmethod
    def reset(cls):
        """
        Resets runtime state.

        Useful for testing.
        """

        with cls._lock:

            cls._classes.clear()
            cls._metadata_registry.clear()
            cls._friend_registry.clear()

            cls._config = {
                "enabled": True,
                "strict": True,
                "debug": False,
            }
