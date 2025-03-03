# Coding style

This page lists the best practices for coding style. We strongly advise you to follow them.

## Python code

- Typing must be used in all classes and functions. Significant updates have been made to typing in the latest Python versions, but these versions are not yet supported on DSS, so please use the typing framework for complex types.
- Docstrings must follow the [Google standard](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings).
- Use a formatter and a linter, such as [Ruff](https://docs.astral.sh/ruff/), to ensure your code is clean and readable.
- Always use absolute imports, and avoid importing any packages in **\_\_init\_\_.py**.
- Always use configuration files, like config.py, JSON configs, or environment variables.
- Use [Poetry](https://python-poetry.org/docs/) to manage dependencies and avoid conflicts you may encounter using pip.
- Write low-code versions of your code to create a recipe plugin, which can be done through additional classes or function wrappers.
- Use [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) to create SQL templates that can be used within your Python methods.

## Unit tests

- Write simple unit tests with good coverage. Instead of testing every single function, focus on creating relevant tests for the main modules.
- Use the [Pytest](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html) framework to write your tests, and take advantage of fixtures by using a **conftest.py** file at the root of your tests.

## Logging

- While Dataiku captures print statements as logs (i.e., stdout), it is better to use logging. You can use the `LoggerManager` developed in the [LVMH Core](https://github.com/lvmh-data/atom-ds-core-library) package.

## Python versioning

[Pyenv](https://github.com/pyenv/pyenv) offers a straightforward method to manage Python versions, whether at the system or project level. It is highly recommended for ML Engineers to develop using Python versions compatible with maison's environments, particularly the available Dataiku Python versions. Currently, we recommend developing on Python 3.9.

For other purposes, we suggest following a general rule of using an n-2 or n-1 major version from the most recent release. For instance, if Python 3.12 is the latest release, consider using 3.10 or 3.11. This approach helps mitigate dependency issues, as many Python packages may face compatibility challenges.

To install Pyenv, please refer to the [installation guidelines](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation). For further information, you can also consult this [article](https://realpython.com/intro-to-pyenv/).