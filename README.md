# 🐍 COBRA

> **Comprehensive Object-Based Runtime Architecture**

[![PyPI](https://img.shields.io/pypi/v/cobra-oop)](https://pypi.org/project/cobra-oop/)
[![Python](https://img.shields.io/pypi/pyversions/cobra-oop)](https://pypi.org/project/cobra-oop/)
[![License](https://img.shields.io/pypi/l/cobra-oop)](LICENSE)

COBRA is an experimental Python framework that introduces **runtime-enforced object-oriented access control** using decorators, descriptors, and runtime introspection.

Unlike Python's naming conventions (`_protected`, `__private`), COBRA validates access **at runtime**, enabling stronger encapsulation without modifying the Python language.

---

# Why COBRA?

Python intentionally embraces the philosophy of:

> *"We're all consenting adults here."*

COBRA explores an alternative approach for projects where **runtime enforcement** of object-oriented design rules is desirable.

The framework currently supports:

- Runtime-enforced private methods
- Runtime-enforced protected methods
- Descriptor-based private fields
- Descriptor-based protected fields
- Runtime policy engine
- Automatic runtime class registration
- Friend access metadata *(v0.3.0)*
- Runtime friend access *(v0.3.1)*

COBRA is designed as a learning project and an extensible runtime architecture for future experimentation.

---

# Features

## ✅ v0.3.1

- Runtime-enforced `@private`
- Runtime-enforced `@protected`
- Descriptor-based `PrivateField`
- Descriptor-based `ProtectedField`
- Friend metadata (`friends=[...]`)
- Runtime friend registry
- Runtime friend access validation
- Centralized runtime access engine
- Policy-based access validation
- Automatic class registration
- Lightweight & dependency-free
- Python 3.11+

---

# Installation

```bash
pip install cobra-oop
```

---

# Quick Start

## Private Members

```python
from cobra import (
    CobraObject,
    PrivateField,
    private,
)


class BankAccount(CobraObject):

    balance = PrivateField(default=1000)

    @private
    def calculate_interest(self):
        return self.balance * 0.08

    def interest(self):
        return self.calculate_interest()


account = BankAccount()

print(account.interest())
```

Output

```text
80.0
```

Attempting

```python
account.calculate_interest()
```

raises

```text
PrivateAccessError
```

---

## Protected Members

```python
from cobra import (
    CobraObject,
    ProtectedField,
    protected,
)


class Animal(CobraObject):

    health = ProtectedField(default=100)

    @protected
    def heartbeat(self):
        return "❤️"

    def check(self):
        return self.heartbeat()


class Dog(Animal):

    def bark(self):
        return self.heartbeat()


dog = Dog()

dog.bark()
```

Attempting

```python
dog.heartbeat()
```

raises

```text
ProtectedAccessError
```

---

# Friend Access *(v0.3.1)*

Friend access allows trusted classes to bypass private or protected restrictions.

```python
from cobra import CobraObject, private


class AccountService(CobraObject):

    def update(self, account):
        return account.update_balance()


class BankAccount(CobraObject):

    @private(
        friends=[AccountService]
    )
    def update_balance(self):
        return "updated"


account = BankAccount()
service = AccountService()

service.update(account)
```

Friend metadata is stored by the decorator and registered automatically
when the `CobraObject` subclass is created.

Non-friend callers are still denied by the runtime access engine.

---

# Current API

```python
from cobra import (

    CobraObject,

    private,
    protected,

    PrivateField,
    ProtectedField,

)
```

---

# Architecture

```text
                Decorators
                     │
                     ▼
            Runtime Access Engine
                     │
                     ▼
              Access Policies
                     │
                     ▼
              Runtime Registry
                     │
     ┌───────────────┴───────────────┐
     ▼                               ▼
 Class Registry              Friend Registry
```

---

# Roadmap

## ✅ v0.1.0

- Runtime private methods
- `@private`
- `CobraObject`

---

## ✅ v0.2.0

- Runtime access engine
- Descriptor-based `PrivateField`
- Runtime class registry
- Policy-based runtime validation

---

## ✅ v0.2.1

- Runtime-enforced `@protected`
- `ProtectedField`
- Expanded automated test suite

---

## 🚧 v0.3.0

- Friend metadata (`friends=[...]`)
- Runtime friend registry
- Friend access validation
- Runtime policy improvements

---

## ✅ v0.3.1

- Automatic friend registration
- Runtime private friend access
- Runtime protected friend access
- Expanded friend test coverage

---

## 🚧 v0.4.0

- `@final`
- `@override`
- Final classes
- Runtime inheritance validation
- Test suite reorganization
- CI/CD integration
- Enhanced documentation

---

## 🚧 v0.5.0

### DOJO

Developer tooling for COBRA.

Planned features include:

- VS Code diagnostics
- Pylance integration
- Architecture validation
- Static analysis
- Runtime contract visualization

---

## 🎯 v1.0.0

Production-ready runtime architecture framework featuring:

- Complete runtime encapsulation
- Stable public API
- Comprehensive documentation
- Friend access
- Runtime contracts
- Architecture enforcement
- Static analysis integration
- Django integration
- FastAPI integration
- Production-ready release

---

# Running Tests

```bash
python -m pytest
```

---

# Contributing

Contributions are welcome.

You can help by:

- Reporting bugs
- Suggesting features
- Improving documentation
- Writing tests
- Submitting pull requests

Please open an issue before beginning large changes.

---

# License

MIT License. See [LICENSE](LICENSE).

---

# Author

**Vishnu Swaroop G**

- GitHub  
  https://github.com/vishnuswaroop21/cobra-oop

- PyPI  
  https://pypi.org/project/cobra-oop/

---

## Inspiration

COBRA began as an exploration after hearing discussions around object-oriented design and the lack of strong encapsulation in Python.

Rather than changing Python itself, COBRA investigates how far runtime-enforced object-oriented principles can be implemented using the language's existing capabilities—decorators, descriptors, and runtime introspection.

The project is both an educational journey into Python's internals and an experimental framework for runtime architecture.
