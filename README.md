# COBRA 🐍

> **Comprehensive Object-Based Runtime Architecture**

**COBRA** is an experimental Python library that introduces **optional runtime-enforced object-oriented programming concepts** while remaining fully compatible with standard Python.

Python follows the philosophy of *"We're all consenting adults here."* COBRA embraces that philosophy while providing developers with the option to enforce stronger object-oriented constraints when building large or enterprise-grade applications.

---

## Why COBRA?

Python intentionally relies on conventions instead of strict access modifiers.

For example:

```python
class BankAccount:
    def __reset_pin(self):
        ...
```

Although name mangling discourages accidental access, private members are still accessible when explicitly referenced.

COBRA explores an alternative approach by introducing optional runtime validation for concepts such as:

* Private methods
* Protected methods
* Private fields
* Final methods
* Runtime contracts
* Interface validation

The goal is **not to replace Python**, but to provide an optional layer of additional runtime guarantees.

---

## Features

### Current (v0.1)

* ✅ `@private`
* ✅ Runtime access validation
* ✅ Custom exception hierarchy
* ✅ Unit tests
* ✅ Extensible architecture

### Planned

* `@protected`
* `PrivateField`
* `ProtectedField`
* `@final`
* `@override`
* Runtime contracts
* Interface support
* Performance optimisations

---

## Installation

```bash
pip install cobra-oop
```

For development:

```bash
pip install -e .
```

---

## Quick Example

```python
from cobra import CobraObject, private


class BankAccount(CobraObject):

    @private
    def reset_pin(self):
        print("PIN reset")

    def change_pin(self):
        self.reset_pin()


account = BankAccount()

account.change_pin()      # ✅ Allowed
account.reset_pin()       # ❌ Raises PrivateAccessError
```

---

## Project Structure

```text
cobra/
├── decorators.py
├── fields.py
├── base.py
├── exceptions.py
├── utils.py
└── __init__.py
```

---

## Roadmap

The development roadmap can be found in:

```
docs/roadmap.md
```

Architecture decisions are documented under:

```
docs/adr/
```

---

## Philosophy

COBRA is designed around a few simple principles:

* Keep Pythonic syntax.
* Make strictness optional.
* Prefer explicit behaviour over hidden magic.
* Build small, testable components.
* Learn by exploring Python internals.

---

## Contributing

Contributions, suggestions, and discussions are always welcome.

If you discover an issue or have an idea for improving COBRA, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License.

---

> *"Python trusts developers. COBRA helps developers trust each other."* 🐍
