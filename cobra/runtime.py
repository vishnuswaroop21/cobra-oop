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


class CobraRuntime:
    """
    Global COBRA runtime.

    A singleton-style runtime used by the access engine.
    """

    _lock = RLock()

    _classes = {}

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
            cls._friend_registry.clear()

            cls._config = {
                "enabled": True,
                "strict": True,
                "debug": False,
            }
