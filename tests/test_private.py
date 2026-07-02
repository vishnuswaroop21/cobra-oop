# tests/test_private.py

import pytest

from cobra import (
    CobraObject,
    PrivateField,
    private,
)
from cobra.exceptions import (
    PrivateAccessError,
)


class Person(CobraObject):

    secret_code = PrivateField(default="XYZ123")

    @private
    def secret(self):
        return "classified"

    def reveal(self):
        return self.secret()

    def reveal_code(self):
        return self.secret_code


class Employee(CobraObject):

    @private
    def salary(self):
        return 50000

    def get_salary(self):
        return self.salary()


class Manager(Employee):

    def manager_salary(self):
        return self.get_salary()


# ---------------------------------------------------------------------
# Method Tests
# ---------------------------------------------------------------------


def test_private_method_can_be_called_inside_class():
    person = Person()

    assert person.reveal() == "classified"


def test_private_method_cannot_be_called_outside_class():
    person = Person()

    with pytest.raises(PrivateAccessError):
        person.secret()


def test_multiple_private_methods():
    employee = Employee()

    assert employee.get_salary() == 50000

    with pytest.raises(PrivateAccessError):
        employee.salary()


# ---------------------------------------------------------------------
# Field Tests
# ---------------------------------------------------------------------


def test_private_field_can_be_accessed_inside_class():
    person = Person()

    assert person.reveal_code() == "XYZ123"


def test_private_field_cannot_be_accessed_outside_class():
    person = Person()

    with pytest.raises(PrivateAccessError):
        _ = person.secret_code


# ---------------------------------------------------------------------
# Inheritance Tests
# ---------------------------------------------------------------------


def test_private_method_still_works_through_public_method():
    manager = Manager()

    assert manager.manager_salary() == 50000


def test_private_method_cannot_be_called_from_subclass_instance():
    manager = Manager()

    with pytest.raises(PrivateAccessError):
        manager.salary()