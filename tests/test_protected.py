# tests/test_protected.py

import pytest

from cobra import (
    CobraObject,
    ProtectedField,
    protected,
)
from cobra.exceptions import (
    ProtectedAccessError,
)


class Animal(CobraObject):

    health = ProtectedField(default=100)

    @protected
    def heartbeat(self):
        return "❤️"

    @protected
    def breathe(self):
        return "Breathing"

    def check(self):
        return self.heartbeat()

    def get_health(self):
        return self.health


class Dog(Animal):

    def bark(self):
        return self.heartbeat()

    def heal(self):
        self.health += 10
        return self.health

    def breathe_test(self):
        return self.breathe()


class Husky(Dog):

    def test(self):
        return self.heartbeat()


# ---------------------------------------------------------------------
# Protected Method Tests
# ---------------------------------------------------------------------


def test_protected_method_can_be_called_inside_class():
    animal = Animal()

    assert animal.check() == "❤️"


def test_protected_method_can_be_called_inside_subclass():
    dog = Dog()

    assert dog.bark() == "❤️"


def test_protected_method_cannot_be_called_outside_class():
    animal = Animal()

    with pytest.raises(ProtectedAccessError):
        animal.heartbeat()


def test_protected_method_cannot_be_called_outside_subclass():
    dog = Dog()

    with pytest.raises(ProtectedAccessError):
        dog.heartbeat()


def test_multiple_protected_methods():
    dog = Dog()

    assert dog.breathe_test() == "Breathing"


def test_grandchild_can_access_protected_method():
    husky = Husky()

    assert husky.test() == "❤️"


# ---------------------------------------------------------------------
# Protected Field Tests
# ---------------------------------------------------------------------


def test_protected_field_can_be_accessed_inside_class():
    animal = Animal()

    assert animal.get_health() == 100


def test_protected_field_can_be_modified_inside_subclass():
    dog = Dog()

    assert dog.heal() == 110


def test_protected_field_cannot_be_accessed_outside_class():
    dog = Dog()

    with pytest.raises(ProtectedAccessError):
        _ = dog.health