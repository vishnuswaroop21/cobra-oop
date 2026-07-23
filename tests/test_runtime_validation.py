# tests/test_runtime_validation.py

import pytest

from cobra import (
    CobraObject,
    CobraRuntime,
    final,
    override,
)
from cobra.exceptions import (
    FinalClassError,
    FinalOverrideError,
    OverrideError,
)


def test_valid_class_is_registered_after_runtime_validation():

    class ValidRuntimeClass(CobraObject):
        pass

    qualified_name = (
        f"{ValidRuntimeClass.__module__}."
        f"{ValidRuntimeClass.__qualname__}"
    )

    assert CobraRuntime.get_class(qualified_name) is ValidRuntimeClass


def test_final_method_override_is_not_registered():

    class RuntimeAnimal(CobraObject):

        @final
        def heartbeat(self):
            return "❤️"

    with pytest.raises(FinalOverrideError):

        class InvalidFinalMethodDog(RuntimeAnimal):

            def heartbeat(self):
                return "💔"

    registered = CobraRuntime.registered_classes()

    assert not any(
        key.endswith("InvalidFinalMethodDog")
        for key in registered
    )


def test_final_class_inheritance_is_not_registered():

    @final
    class RuntimeAnimal(CobraObject):
        pass

    with pytest.raises(FinalClassError):

        class InvalidFinalClassDog(RuntimeAnimal):
            pass

    registered = CobraRuntime.registered_classes()

    assert not any(
        key.endswith("InvalidFinalClassDog")
        for key in registered
    )


def test_invalid_override_is_not_registered():

    class RuntimeAnimal(CobraObject):
        pass

    with pytest.raises(OverrideError):

        class InvalidOverrideDog(RuntimeAnimal):

            @override
            def run(self):
                return "Running"

    registered = CobraRuntime.registered_classes()

    assert not any(
        key.endswith("InvalidOverrideDog")
        for key in registered
    )


def test_runtime_stores_final_method_metadata():

    class RuntimeAnimal(CobraObject):

        @final
        def heartbeat(self):
            return "❤️"

    registry = CobraRuntime._metadata_registry

    assert registry[RuntimeAnimal]["heartbeat"]["final"] is True


def test_runtime_stores_override_metadata():

    class RuntimeAnimal(CobraObject):

        def speak(self):
            return "..."

    class RuntimeDog(RuntimeAnimal):

        @override
        def speak(self):
            return "Woof"

    registry = CobraRuntime._metadata_registry

    assert registry[RuntimeDog]["speak"]["override"] is True


def test_final_override_takes_priority_over_override_validation():

    class RuntimeAnimal(CobraObject):

        @final
        def heartbeat(self):
            return "❤️"

    with pytest.raises(FinalOverrideError):

        class RuntimeDog(RuntimeAnimal):

            @override
            def heartbeat(self):
                return "💔"
