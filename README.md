# 🐍 COBRA

> **Comprehensive Object-Based Runtime Architecture**

COBRA is an experimental Python library that brings runtime encapsulation and object-oriented access control to Python using decorators, descriptors, and runtime inspection.

Unlike Python's naming conventions (`_protected`, `__private`), COBRA enforces access restrictions at runtime.

---

## Features

### ✅ v0.2.0

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

### ✅ v0.1

- Runtime private methods

### ✅ v0.2

- Descriptor-based private fields
- Runtime access engine
- Runtime class registry

### 🚧 v0.3

- Protected methods
- Protected fields
- Friend access
- Runtime policy improvements

### 🚧 v0.4

- Final methods
- Final classes
- Runtime validation

### 🎯 v1.0

- Complete runtime encapsulation framework
- Architecture enforcement
- Static analysis integration
- Framework integrations (Django, FastAPI)

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