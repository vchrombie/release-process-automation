# release-process-automation

Automating the Release process using [Bitergia/release-tools](https://github.com/Bitergia/release-tools), [Poetry](https://python-poetry.org/), and [GitHub Actions](https://docs.github.com/en/actions).

This work was designed and implemented for the GrimoireLab toolset. As of now, the whole workflow is supported only for Python projects. But, this can be tailored and used for any project.

This work is licensed under GPL3 or later.

## Features

This combination of the tools allows us to:
- manage your releases of your python project with proper versioning and release notes
- build the packages and test them against the test suite
- publish packages to PyPI

## Requirements

- Poetry should be configured to your Python project. The `pyproject.toml` file must also be tracked on your repository. See [The pyproject.toml file | Documentation | Poetry](https://python-poetry.org/docs/pyproject/) for more information.
- The project should have a `_version.py` file. This file must also be tracked on your repository. It must contain a variable named `__version__`. The value must be a string following semantic versioning format.
```
$ cat _version.py
__version__ = "3.6.5"
```
- The project should have `NEWS` and `AUTHORS` files.
- Projected should be hosted on GitHub as we use GitHub Actions.

## Workflow


