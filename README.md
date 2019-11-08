# serdataclasses

*Warning: vaporware, subject to change at any time, for any reason, in any way.*

This library has two goals:

1. Deserialize JSON into python dataclasses
2. Serialize Python data classes into JSON

It has no external dependencies. Python 3.8+.

## Notes

* Recursive types aren't currently supported by mypy. I intend to wait until they are before releasing this library.
* Edge cases haven't been considered. This library is a learning project, for now.
* Inspired by [undictify](https://github.com/Dobiasd/undictify), but special-cased to dataclasses and more-focused on serde instead of general function signature overrides.

## Written by

* Samuel Roeca
