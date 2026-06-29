# tests/test_private.py

import pytest

from cobra import CobraObject, private
from cobra.exceptions import PrivateAccessError


class Person(CobraObject):

    @private
    def secret(self):
        return "classified"

    def reveal(self):
        return self.secret()


class Employee(CobraObject):

    @private
    def salary(self):
        return 50000

    def get_salary(self):
        return self.salary()


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