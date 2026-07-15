# tests/test_friend.py

import pytest

from cobra import (
    CobraObject,
    CobraRuntime,
    private,
)
from cobra.exceptions import (
    PrivateAccessError,
)


# ---------------------------------------------------------------------
# Test Classes
# ---------------------------------------------------------------------


class AccountService(CobraObject):
    pass


class AuditService(CobraObject):
    pass


class Hacker(CobraObject):
    pass


class BankAccount(CobraObject):

    @private(friends=[AccountService])
    def account_number(self):
        return "123456789"

    @private(
        friends=[
            AccountService,
            AuditService,
        ]
    )
    def balance(self):
        return 1000

    def reveal_account(self):
        return self.account_number()

    def reveal_balance(self):
        return self.balance()


# ---------------------------------------------------------------------
# Decorator Metadata
# ---------------------------------------------------------------------


def test_private_accepts_single_friend():

    metadata = BankAccount.account_number.__cobra_metadata__

    assert metadata["friends"] == frozenset(
        {AccountService}
    )


def test_private_accepts_multiple_friends():

    metadata = BankAccount.balance.__cobra_metadata__

    assert metadata["friends"] == frozenset(
        {
            AccountService,
            AuditService,
        }
    )


def test_private_without_friends():

    class User(CobraObject):

        @private
        def secret(self):
            return "ok"

    metadata = User.secret.__cobra_metadata__

    assert metadata["friends"] == frozenset()


# ---------------------------------------------------------------------
# Existing Behaviour
# ---------------------------------------------------------------------


def test_private_method_still_works_inside_class():

    account = BankAccount()

    assert account.reveal_account() == "123456789"


def test_private_method_still_denies_external_access():

    account = BankAccount()

    with pytest.raises(PrivateAccessError):
        account.account_number()


# ---------------------------------------------------------------------
# Runtime Registration
# ---------------------------------------------------------------------


def test_runtime_register_friend():

    CobraRuntime.register_friend(
        owner=BankAccount,
        member="account_number",
        friends=[AccountService],
    )

    friends = CobraRuntime.get_friends(
        owner=BankAccount,
        member="account_number",
    )

    assert friends == frozenset(
        {AccountService}
    )


def test_runtime_multiple_friends():

    CobraRuntime.register_friend(
        owner=BankAccount,
        member="balance",
        friends=[
            AccountService,
            AuditService,
        ],
    )

    friends = CobraRuntime.get_friends(
        owner=BankAccount,
        member="balance",
    )

    assert friends == frozenset(
        {
            AccountService,
            AuditService,
        }
    )


def test_runtime_unknown_member_returns_empty_set():

    friends = CobraRuntime.get_friends(
        owner=BankAccount,
        member="does_not_exist",
    )

    assert friends == frozenset()


# ---------------------------------------------------------------------
# Future Friend Access
# ---------------------------------------------------------------------

#
# These tests are intentionally postponed until
# friend access validation is implemented.
#
# def test_friend_can_call_private():
#     ...
#
# def test_non_friend_cannot_call_private():
#     ...
#
# def test_friend_can_call_protected():
#     ...
#
# def test_friend_inheritance():
#     ...
#