# pyproject-autoflake

[![PyPI version](https://badge.fury.io/py/pyproject-autoflake.svg)](https://badge.fury.io/py/pyproject-autoflake) [![Python Versions](https://img.shields.io/pypi/pyversions/pyproject-autoflake.svg)](https://pypi.org/project/pyproject-autoflake/)

**pyproject-autoflake** (**pautoflake**), a monkey patching wrapper to connect [autoflake](https://github.com/myint/autoflake) with pyproject.toml configuration.

## Motivation

The original autoflake does not support configuration files such as pyproject.toml.
This is slightly inconvenient for modern Python development.

pautoflake is a thin wrapper library that calls autoflake with a configuration read from pyproject.toml.

pyproject-autoflake is inspired by [pyproject-flake8](https://github.com/csachs/pyproject-flake8). Many thanks! 😉

## Installation

### pip

```sh
pip install pyproject-autoflake
```

### poetry

```sh
poetry add -D pyproject-autoflake
```

## Usage

At first, you add `[tool.autoflake]` in your pyproject.toml.

```toml
# pyproject.toml

...

[tool.autoflake]
# return error code if changes are needed
check = false
# make changes to files instead of printing diffs
in-place = true
# drill down directories recursively
recursive = true
# exclude file/directory names that match these comma-separated globs
exclude = "<GLOBS>"
# by default, only unused standard library imports are removed; specify a comma-separated list of additional
# modules/packages
imports = "<IMPORTS>"
# expand wildcard star imports with undefined names; this only triggers if there is only one star import in
# the file; this is skipped if there are any uses of `__all__` or `del` in the file
expand-star-imports = true
# remove all unused imports (not just those from the standard library)
remove-all-unused-imports = true
# exclude __init__.py when removing unused imports
ignore-init-module-imports = true
# remove all duplicate keys in objects
remove-duplicate-keys = true
# remove unused variables
remove-unused-variables = true
# print more verbose logs (larger numbers are more verbose)
verbose = 0

...

```

Second, you call **p**autoflake.

```bash
pautoflake sample.py
```

## License

[MIT License](./LICENSE)
