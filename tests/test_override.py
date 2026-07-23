# tests/test_override.py

import pytest

from cobra import (
    CobraObject,
    override,
)
from cobra.exceptions import OverrideError


def test_override_metadata_is_stored():

    class Animal(CobraObject):

        def speak(self):
            return "..."

    class Dog(Animal):

        @override
        def speak(self):
            return "Woof"

    metadata = Dog.speak.__cobra_metadata__

    assert metadata["override"] is True


def test_valid_override_succeeds():

    class Animal(CobraObject):

        def speak(self):
            return "..."

    class Dog(Animal):

        @override
        def speak(self):
            return "Woof"

    dog = Dog()

    assert dog.speak() == "Woof"


def test_invalid_override_raises_override_error():

    class Animal(CobraObject):
        pass

    with pytest.raises(OverrideError):

        class Dog(Animal):

            @override
            def run(self):
                return "Running"


def test_invalid_override_error_happens_during_class_creation():

    class Animal(CobraObject):
        pass

    with pytest.raises(OverrideError):

        class Dog(Animal):

            @override
            def run(self):
                return "Running"

    assert "Dog" not in locals()


def test_override_can_target_grandparent_method():

    class Animal(CobraObject):

        def speak(self):
            return "..."

    class Mammal(Animal):
        pass

    class Dog(Mammal):

        @override
        def speak(self):
            return "Woof"

    dog = Dog()

    assert dog.speak() == "Woof"


def test_method_without_override_remains_backward_compatible():

    class Animal(CobraObject):

        def speak(self):
            return "..."

    class Dog(Animal):

        def speak(self):
            return "Woof"

    dog = Dog()

    assert dog.speak() == "Woof"
