# Changelog

## v0.3.0

### Added

- Added `friends=[...]` support to `@private`
- Added `friends=[...]` support to `@protected`
- Added runtime friend registry (`CobraRuntime`)
- Added friend metadata for runtime access policies
- Extended runtime architecture for friend access
- Added friend registration APIs
- Added initial friend unit test suite
- Maintained backward compatibility with existing decorators

---

## v0.2.1

### Added

- Added `@protected` decorator
- Added `ProtectedField`
- Added protected runtime access validation
- Expanded protected access test suite
- Increased automated test coverage to **16 passing tests**

---

## v0.2.0

### Added

- Added runtime access engine
- Added descriptor-based `PrivateField`
- Added runtime class registry (`CobraRuntime`)
- Introduced runtime access policies
- Refactored decorators to use the centralized access engine
- Added support for runtime field encapsulation
- Improved project architecture and package organization
- Added comprehensive unit tests for private methods and fields
- Published COBRA on PyPI

---

## v0.1.0

### Added

- Initial release
- Added `@private` decorator
- Added `CobraObject`
- Added `PrivateField` placeholder
- Added custom exceptions
- Added initial unit tests