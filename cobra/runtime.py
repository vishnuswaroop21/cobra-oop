"""
cobra.runtime

COBRA runtime.

Responsible for:

- Class registration
- Runtime configuration
- Future plugin management
- Future friend resolution
"""

from threading import RLock


class CobraRuntime:
    """
    Global COBRA runtime.

    A singleton-style runtime used by the access engine.
    """

    _lock = RLock()

    _classes = {}

    _config = {
        "enabled": True,
        "strict": True,
        "debug": False,
    }

    @classmethod
    def register_class(cls, target):
        """
        Registers a CobraObject subclass.
        """

        with cls._lock:
            key = f"{target.__module__}.{target.__qualname__}"
            cls._classes[key] = target

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

    @classmethod
    def reset(cls):
        """
        Resets runtime state.

        Useful for testing.
        """

        with cls._lock:
            cls._classes.clear()

            cls._config = {
                "enabled": True,
                "strict": True,
                "debug": False,
            }