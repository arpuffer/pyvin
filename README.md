# PyVIN
A Vehicle Identification Number (VIN) decoder for Python.  This leverages the NHTSA API to decode VINs into collections of vehicle data that can be easily explored (https://vpic.nhtsa.dot.gov/api/)

## Installation

Requires Python 3.10 or newer. Add the library to a uv project with `uv add pyvin`,
or install it with `pip install pyvin`.

## Development

Install uv, then run these commands from the repository root:

```sh
uv sync --locked
uv run pytest --cov=src/pyvin --cov-fail-under=92 tests/unit/ -vv
uv run pylint src/pyvin
uv run flake8 src/pyvin
uv run mypy src/pyvin
uv build
```

The default development command above and CI run only `tests/unit/`. These tests
use mocked vPIC responses and block real HTTP requests.

Run the live vPIC integration tests separately when network access and the NHTSA
service are available:

```sh
uv run pytest tests/integration/ -vv
```

Running `pytest` without a test path discovers both suites, including live API tests.

The `.python-version` file selects Python 3.14 for local development; CI checks
Python 3.10 through 3.14. Use `uv sync --python 3.10` to select another version.

Dependencies live in `pyproject.toml`; commit `uv.lock` for reproducible development
and CI environments. Use `uv add <package>` for runtime dependencies,
`uv add --dev <package>` for development tools, and `uv lock --upgrade` to update
the lockfile. `uv sync --no-dev` installs only the library and runtime dependencies.

## Releasing

The `publish.yml` workflow publishes to PyPI when a version tag such as `v0.0.4`
is pushed. A version change or merge alone does not publish anything. It runs the
code checks and offline unit tests on Python 3.10 through 3.14, verifies that the
tag exactly matches `v` plus the version in `pyproject.toml`, and builds the wheel
and source distribution before publishing.

Before the first release, create a GitHub environment named `pypi`. In the PyPI
project's Publishing settings, add a GitHub Trusted Publisher with these values:

- Owner: `arpuffer`
- Repository: `pyvin`
- Workflow filename: `publish.yml`
- Environment: `pypi`

See the [PyPI Trusted Publisher setup guide](https://docs.pypi.org/trusted-publishers/adding-a-publisher/).
No PyPI API token is needed.

For each release:

1. Update the version in `pyproject.toml` and `src/pyvin/__init__.py` to the same
   new, unused version, then run `uv lock`.
2. Commit and merge the version changes and lockfile into `main`.
3. Tag the merged commit and push the tag (for example, `git tag v0.0.4` followed
   by `git push origin v0.0.4`).

## Basic Usage:
```
In [0]: from pyvin import VIN

In [1]: vehicle = VIN('JT2AE09W4P0038539')

In [2]: (vehicle.Make, vehicle.Model, vehicle.ModelYear)
Out[2]: ('TOYOTA', 'Corolla', '1993')

In [3]: my_vins = ('JT2AE09W4P0038539', 'KMHD35LH5EU205042')

In [4]: my_vehicles = VIN(*my_vins)

In [5]: for veh in my_vehicles:
   ...:     print(veh.Make, veh.Model, veh.ModelYear)
TOYOTA Corolla 1993
HYUNDAI Elantra 2014
```

## Advanced Usage:
The user can also specify how invalid VINs are handled, be it raising an exception or ignoring them:
```
In [6]: import pyvin
In [7]: new_car = pyvin.VIN('Foo', error_handling=pyvin.RAISE)
Out[7]: VINError: Invalid char "o"the u
```

To simply clean a VIN list, with no decoding involved, the following can be called:
```
In [8]: import pyvin

In [9]: my_vins = ('JT2AE09W4P0038539', 'Foo')

In [10]: cleaned_vins = pyvin.clean_vins(my_vins)

In [11]: cleaned_vins
Out[11]: ['JT2AE09W4P0038539']
```
For simple validation, no calls to the NHTSA API are used, as there is a formula to validate VINs
