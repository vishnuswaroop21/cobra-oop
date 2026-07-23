# tests/test_final.py

import pytest

from cobra import (
    CobraObject,
    final,
)
from cobra.exceptions import (
    FinalClassError,
    FinalOverrideError,
)


def test_final_method_metadata_is_stored():

    class Animal(CobraObject):

        @final
        def heartbeat(self):
            return "❤️"

    metadata = Animal.heartbeat.__cobra_metadata__

    assert metadata["final"] is True


def test_final_method_can_be_called_normally():

    class Animal(CobraObject):

        @final
        def heartbeat(self):
            return "❤️"

    animal = Animal()

    assert animal.heartbeat() == "❤️"


def test_final_method_cannot_be_overridden():

    class Animal(CobraObject):

        @final
        def heartbeat(self):
            return "❤️"

    with pytest.raises(FinalOverrideError):

        class Dog(Animal):

            def heartbeat(self):
                return "💔"


def test_final_method_error_happens_during_class_creation():

    class Animal(CobraObject):

        @final
        def heartbeat(self):
            return "❤️"

    with pytest.raises(FinalOverrideError):

        class Dog(Animal):

            def heartbeat(self):
                return "💔"

    assert "Dog" not in locals()


def test_final_class_metadata_is_stored():

    @final
    class Animal(CobraObject):
        pass

    metadata = Animal.__cobra_metadata__

    assert metadata["final"] is True


def test_final_class_cannot_be_inherited():

    @final
    class Animal(CobraObject):
        pass

    with pytest.raises(FinalClassError):

        class Dog(Animal):
            pass


def test_final_class_error_happens_during_class_creation():

    @final
    class Animal(CobraObject):
        pass

    with pytest.raises(FinalClassError):

        class Dog(Animal):
            pass

    assert "Dog" not in locals()


def test_non_overridden_final_method_allows_subclass_creation():

    class Animal(CobraObject):

        @final
        def heartbeat(self):
            return "❤️"

    class Dog(Animal):

        def bark(self):
            return "Woof"

    dog = Dog()

    assert dog.heartbeat() == "❤️"
    assert dog.bark() == "Woof"
