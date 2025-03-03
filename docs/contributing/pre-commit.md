# Git hooks with Pre-commit

Pre-commit is a framework for managing and maintaining multi-language pre-commit hooks. It ensures that your code meets the required standards before committing. This framework provides several safeguards to enhance code quality and consistency, including:

- **Preventing the commit of private keys**: Ensures sensitive data like private keys are not accidentally committed.
- **Preventing commits on the main branch**: Enforces branching strategies to maintain a clean main branch.
- **Preventing the commit of large files (more than 1000KB)**: Helps avoid adding excessively large files to the repository.
- **Providing a code formatter and linter through Ruff**: Ensures consistent code style and catches common errors.
- **Providing a docstring coverage checker through Interrogate**: Ensures that all functions and classes have appropriate documentation.
- **Providing a dependencies export through Poetry**: Manages and locks dependencies, ensuring consistent environments.

*Ruff* is a fast code linting and formatting tool, written in Rust, designed to replace tools like Black, Flake8, and Isort.
*Interrogate* checks for missing docstrings in the codebase, ensuring proper documentation coverage.
*Poetry* is a dependency management tool that also manages virtual environments.

## Installation

Pre-commit is normally installed automatically if you use the `task init` command. Otherwise, you can install it manually with the following command:

```sh
poetry run pre-commit install
```

Ensure you have run the `poetry install` command first to install all dependencies. In short, it is strongly recommended to use:

```sh
task init
```

If you are unsure how to use Task, refer to the **Tasks page** for guidance.

## Pre-commit configuration

Pre-commit is configured in the `.pre-commit-config.yaml` file, located at the root of the project. Some tools like Ruff and Interrogate are referenced in this file but are configured in the `pyproject.toml` file.

The base configuration is as follows:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.3.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
        args: [--maxkb=1000]
      - id: check-merge-conflict
      - id: trailing-whitespace
      - id: no-commit-to-branch
        args: [--branch, main]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.7
    hooks:
      - id: ruff
        args: [--config, pyproject.toml]
      - id: ruff-format
        args: [--config, pyproject.toml]

  - repo: https://github.com/python-poetry/poetry
    rev: 1.4.0
    hooks:
      - id: poetry-lock
      - id: poetry-export
        args:
          [
            "--without-hashes",
            "-f",
            "requirements.txt",
            "-o",
            "code-env/python/spec/requirements.txt",
          ]
        verbose: true

  - repo: https://github.com/econchick/interrogate
    rev: 1.5.0
    hooks:
      - id: interrogate
        args: [--config, pyproject.toml]
```

For more detailed information, visit the [official Pre-commit documentation](https://pre-commit.com) and see the [list of available hooks](https://pre-commit.com/hooks.html).
