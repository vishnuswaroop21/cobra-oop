# 🐍 COBRA

> **Comprehensive Object-Based Runtime Architecture**

COBRA is an experimental Python library that brings runtime encapsulation and object-oriented access control to Python using decorators, descriptors, and runtime inspection.

Unlike Python's naming conventions (`_protected`, `__private`), COBRA enforces access restrictions at runtime.

---

## Features

### ✅ v0.2.1

- Runtime enforced private methods
- Descriptor-based private fields
- Runtime access engine
- Automatic class registration
- Lightweight and dependency-free
- Python 3.11+

---

## Installation

```bash
pip install cobra-oop
```

---

## Example

```python
from cobra import CobraObject, PrivateField, private


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

```
80.0
```

Attempting to access private members directly:

```python
account.calculate_interest()
```

raises

```
PrivateAccessError
```

Likewise,

```python
account.balance
```

raises

```
PrivateAccessError
```

---

## Current API

```python
from cobra import (
    CobraObject,
    PrivateField,
    private,
)
```

---

## Roadmap

### ✅ v0.1.0

- Runtime private methods
- `@private` decorator
- `CobraObject`

### ✅ v0.2.0

- Descriptor-based private fields
- Runtime access engine
- Runtime class registry
- Runtime access policies
- `PrivateField`

### ✅ v0.2.1

- `@protected` decorator
- `ProtectedField`
- Protected runtime validation
- Expanded automated test suite (16 tests)

### 🚧 v0.3.0

- `@friend` decorator
- `FriendField`
- Friend registry
- Friend access policy
- Runtime policy enhancements

### 🚧 v0.4.0

- `@final` decorator
- `@override` decorator
- Final classes
- Test suite reorganization
- CI/CD integration
- Improved documentation

### 🚧 v0.5.0

- DOJO static analysis engine
- VS Code / Pylance diagnostics
- Architecture rules
- Runtime contracts
- Developer tooling

### 🎯 v1.0.0

- Complete runtime encapsulation framework
- Stable public API
- Comprehensive documentation
- Architecture enforcement
- Static analysis integration
- Framework integrations (Django, FastAPI)
- Production-ready release

---

## Running Tests

```bash
python -m pytest
```

---

## Contributing

Contributions, bug reports, feature requests, and design discussions are welcome.

Please open an issue before starting major changes.

---

## License

MIT License

---

## Author

**Vishnu Swaroop**

GitHub:
https://github.com/vishnuswaroop21/cobra-oop

PyPI:
https://pypi.org/project/cobra-oop/