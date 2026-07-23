# tests/test_friend.py

import pytest

from cobra import (
    CobraObject,
    CobraRuntime,
    private,
    protected,
)
from cobra.exceptions import (
    PrivateAccessError,
    ProtectedAccessError,
)


# ---------------------------------------------------------------------
# Test Classes
# ---------------------------------------------------------------------


class AccountService(CobraObject):

    def read_account_number(self, account):
        return account.account_number()

    def read_balance(self, account):
        return account.balance()

    def read_routing_code(self, account):
        return account.routing_code()


class PremiumAccountService(AccountService):
    pass


class AuditService(CobraObject):

    def read_balance(self, account):
        return account.balance()


class Hacker(CobraObject):

    def read_account_number(self, account):
        return account.account_number()

    def read_routing_code(self, account):
        return account.routing_code()


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

    @protected(friends=[AccountService])
    def routing_code(self):
        return "ROUTE-001"


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


def test_protected_accepts_friend():

    metadata = BankAccount.routing_code.__cobra_metadata__

    assert metadata["friends"] == frozenset(
        {AccountService}
    )


def test_friend_metadata_preserves_access_type():

    metadata = BankAccount.account_number.__cobra_metadata__

    assert metadata["access"].name == "PRIVATE"


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


def test_runtime_empty_registry_returns_empty_dict(monkeypatch):

    monkeypatch.setattr(
        CobraRuntime,
        "_friend_registry",
        {},
    )

    assert CobraRuntime.registered_friends() == {}


def test_runtime_unknown_owner_returns_empty_set():

    class UnknownOwner(CobraObject):
        pass

    friends = CobraRuntime.get_friends(
        owner=UnknownOwner,
        member="account_number",
    )

    assert friends == frozenset()


def test_runtime_is_friend_returns_true_for_registered_friend():

    service = AccountService()

    assert CobraRuntime.is_friend(
        owner=BankAccount,
        member="account_number",
        caller=service,
    )


def test_runtime_is_friend_returns_false_for_non_friend():

    hacker = Hacker()

    assert not CobraRuntime.is_friend(
        owner=BankAccount,
        member="account_number",
        caller=hacker,
    )


def test_runtime_registry_inspection_contains_owner():

    registry = CobraRuntime.registered_friends()

    assert BankAccount in registry


def test_runtime_registry_inspection_contains_member():

    registry = CobraRuntime.registered_friends()

    assert "account_number" in registry[BankAccount]


def test_automatic_runtime_registration_single_friend():

    friends = CobraRuntime.get_friends(
        owner=BankAccount,
        member="account_number",
    )

    assert friends == frozenset(
        {AccountService}
    )


def test_automatic_runtime_registration_multiple_friends():

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


# ---------------------------------------------------------------------
# Friend Access Validation
# ---------------------------------------------------------------------


def test_friend_can_call_private_method():

    service = AccountService()
    account = BankAccount()

    assert service.read_account_number(account) == "123456789"


def test_multiple_friends_can_call_private_method():

    account_service = AccountService()
    audit_service = AuditService()
    account = BankAccount()

    assert account_service.read_balance(account) == 1000
    assert audit_service.read_balance(account) == 1000


def test_non_friend_cannot_call_private_method():

    hacker = Hacker()
    account = BankAccount()

    with pytest.raises(PrivateAccessError):
        hacker.read_account_number(account)


def test_inherited_friend_can_call_private_method():

    service = PremiumAccountService()
    account = BankAccount()

    assert service.read_account_number(account) == "123456789"


def test_friend_can_call_protected_method():

    service = AccountService()
    account = BankAccount()

    assert service.read_routing_code(account) == "ROUTE-001"


def test_non_friend_cannot_call_protected_method():

    hacker = Hacker()
    account = BankAccount()

    with pytest.raises(ProtectedAccessError):
        hacker.read_routing_code(account)
