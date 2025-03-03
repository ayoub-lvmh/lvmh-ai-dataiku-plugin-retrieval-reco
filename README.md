# lvmh-ai-dataiku-plugin-retrieval-reco

This repository contains the deep2tower Dataiku plugin.

## Plugin architecture

    .
    ├── .github
    │     ├── actions/setup
    │     │     └── action.yaml                 <---------- GitHub Action to setup Python and Poetry
    │     └── workflows
    │           ├── github-actions.yml          <---------- CI/CD to run unit test, linter, formatter, ect.
    │           │
    │           ├── mkdocs-build.yml            <---------- CI/CD to build and deploy documentation.
    │           │
    │           └── semantic-release.yml        <---------- CI/CD to create and deploy semantic release.
    │
    ├── code-env
    │     └── python
    │           ├── spec
    │           │     └──requirements.txt       <---------- Dependencies listed with versions.
    │           │
    │           └── desc.json                   <---------- JSON file to specify which Python interpreter to use,
    │                                                       if to use pip or conda for package installation and if
    │                                                       jupyter notebook will be intialized at the start.
    │
    ├── custom-recipes
    │     └── template-recipe
    │           ├── recipe.json                 <---------- JSON file containing the parameters of a placehoder recipe.
    │           │
    │           └── recipe.py                   <---------- Placehoder python file meant to be used by the recipe.
    │
    ├── docs                                    <---------- Directory of .md files that will be used to build docs.
    │
    ├── python-lib                              <---------- Directory of funcs that will be reused through the plugin.
    │     └── deep2tower
    │           ├── __init__.py
    │           │
    │           ├── src                         <---------- Directory that contains main functions, base module and
    │           │                                           utilities.
    │           │
    │           └── tests                       <---------- Directory of unit test.
    │
    ├── tasks                                   <---------- Tasks files helpers.
    │
    ├── .gitignore
    │
    ├── .pre-commit-config.yaml                 <---------- The Git hooks to use at the pre-commit stage.
    │
    ├── .python-version                         <---------- The Python version to use.
    │
    ├── mkdocs.yaml                             <---------- Configuration files to build the docs.
    │
    ├── plugin.json                             <---------- The plugin JSON file containing all high level information
    │                                                       such as plugin_id, pluginn version, description, etc.
    │
    ├── poetry.lock                             <---------- The locked dependencies of the project.
    │
    ├── poetry.toml                             <---------- Configuration file for poetry backend.
    │
    ├── pyproject.toml                          <---------- The project configuration, it contains the project
    │                                                       information, dependencies, configuration and the pre-commit
    │                                                       configurations for ruff and interrogate.
    │
    ├── README.md
    │
    ├── CHANGELOG.md
    │
    └── taskfile.yaml                           <---------- Task file that contains commands as build tool.

## Coding guideline

This section lists the best practices for coding style. We strongly advise you to follow them.

### Coding style

- Typing must be used in all classes and functions. Significant updates have been made to typing in the latest Python versions, but these versions are not yet supported on DSS, so please use the typing framework for complex types.
- Docstrings must follow the [Google standard](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings).
- Use a formatter and a linter, such as [Ruff](https://docs.astral.sh/ruff/), to ensure your code is clean and readable.
- Always use absolute imports, and avoid importing any packages in **\_\_init\_\_.py**.
- Always use configuration files, like config.py, JSON configs, or environment variables.
- Use [Poetry](https://python-poetry.org/docs/) to manage dependencies and avoid conflicts you may encounter using pip.
- Write low-code versions of your code to create a recipe plugin, which can be done through additional classes or function wrappers.
- Use [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) to create SQL templates that can be used within your Python methods.

### Unit tests

- Write simple unit tests with good coverage. Instead of testing every single function, focus on creating relevant tests for the main modules.
- Use the [Pytest](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html) framework to write your tests, and take advantage of fixtures by using a **conftest.py** file at the root of your tests.

### Logging

- While Dataiku captures print statements as logs (i.e., stdout), it is better to use logging. You can use the `LoggerManager` developed in the [LVMH Core](https://github.com/lvmh-data/atom-ds-core-library) package.

### Python versioning

[Pyenv](https://github.com/pyenv/pyenv) offers a straightforward method to manage Python versions, whether at the system or project level. It is highly recommended for ML Engineers to develop using Python versions compatible with maison's environments, particularly the available Dataiku Python versions. Currently, we recommend developing on Python 3.9.

For other purposes, we suggest following a general rule of using an n-2 or n-1 major version from the most recent release. For instance, if Python 3.12 is the latest release, consider using 3.10 or 3.11. This approach helps mitigate dependency issues, as many Python packages may face compatibility challenges.

To install Pyenv, please refer to the [installation guidelines](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation). For further information, you can also consult this [article](https://realpython.com/intro-to-pyenv/).

## Contributing

This section provides guidelines and best practices for contributing to the project, including how to collaborate effectively on GitHub, use continuous integration tools, and manage dependencies.

### Collaborating on GitHub

Working with GitHub involves using Git, making clear commits, managing branches correctly, and using tags effectively. Here are some guidelines:

**Commits:**

Avoid long commits and aim for smaller, easier-to-understand commit messages. Write one commit per changed file, following this template:
```
<type>: <description>
```
Where `<type>` can be one of the following:
- `add`: Adding new files or components
- `feat`: Feature creation - *Used by semantic release*
- `fix`: Bug fixing - *Used by semantic release*
- `perf`: Performance improvements - *Used by semantic release*
- `ci`: Continuous Integration updates
- `refactor`: Code refactoring with no new features or bug fixes
- `docs`: Documentation updates
- `test`: Adding new tests and/or correcting previous ones
- `revert`: Reverting to a previous commit
- `conf`: Configuration updates
- `rm`: Remove files
- `build`: Build system
- `merge`: Merge branches or resolve merge conflicts
- `style`: Code style or formatting changes

For example:
```
docs: Adding some best practices elements to README.md
```

**Branches:**

Use `<type>/<name>` for your branches, where `<type>` can be one of the following:
- `feat` or `feature`: New feature
- `fix`: Bug fix
- `docs`: Changes to the documentation
- `style`: Formatting, linting; no production code change
- `refactor`: Refactoring production code
- `test`: Adding missing tests, refactoring tests

**Tags:**

Use an vX.Y.Z pattern, where X is for major releases, Y is for new features, and Z is for bug fixes. When pushing a new tag, remember to always provide a release with it!

**Pull Requests:**

Ensure you have the right code reviewers when creating your pull request. Use pre-commits and CI to create better PRs.

**Issues:**

Utilize GitHub issues to request changes or share bug reports with the packaging team responsible for modifying the main branch.

### Continuous integration / Continous development

**Pre-commit:**

Pre-commit is a framework for managing and maintaining multi-language pre-commit hooks. It helps to ensure that your code meets the required standards before committing. It provides several guardrails such as:
- Preventing the commit of private keys
- Preventing commits on the main branch
- Preventing the commit of large files (more than 1000KB)
- Providing a code formatter and linter through Ruff
- Providing a docstring coverage checker through Interrogate
- Providing a dependencies export through Poetry

*Ruff is a fast code linting and formatting tool, written in Rust, set to replace tools like Black, Flake8, and Isort.*
*Interrogate is a checker for missing docstrings in the codebase.*
*Poetry is a dependency management tool.*

**GitHub Actions:**

GitHub Actions is a Continuous Integration/Continuous Development (CI/CD) tool. For more information, see the [official documentation](https://docs.github.com/en/actions).

For plugin development, we utilize CI/CD to enforce code quality standards and streamline the release process. Our CI pipeline ensures that every merge request passes through a series of checks, including:
- Linters and Formatters: We run Ruff for both linting and formatting to maintain a consistent and clean codebase.
- Docstring Validation: We use Interrogate to verify that the code is properly documented with required docstrings.
- Unit Tests: Comprehensive unit tests are executed to ensure no regressions or functional issues are introduced.

In addition to these quality checks, we automate our release process using Semantic Release. This system manages versioning, updates tags, generates the CHANGELOG, and creates new releases based on commit messages, making the release process consistent and error-free.

Our CI/CD also handles documentation using MkDocs. It automatically builds and deploys the latest documentation to a dedicated `gh-pages` branch, ensuring it is continuously updated and accessible via GitHub Pages.

### Dependencies management

Poetry is a tool for dependency management and packaging in Python. It helps manage dependencies and virtual environments efficiently.

It also allows us to define and configure tools like Ruff and Interrogate. Note that Poetry is configured through the `poetry.toml` to create in-project virtual environments.

> [!IMPORTANT]
> **Ensure you follow these guidelines to maintain consistency, code quality, and efficient collaboration within the project.**

## Documentation

The functional documentation is stored on Confluence in the [Electron space](https://lvmh-maisons.atlassian.net/wiki/spaces/POEM/overview).

The technical documenration is build using Mkdocs framework and stored on GitHub pages. MkDocs is a fast, simple and downright gorgeous static site generator that's geared towards building project documentation. Documentation source files are written in Markdown, and configured with a single YAML configuration file.
The `mkdocs.yaml` file at the root of the repository is the configuration file for the MkDocs framework. The primary modification you may need to make is under the **nav** key, which is used to order pages and map them to the associated Markdown files.

The `docs/` folder contains the documentation source files. Each Markdown file is linked to a page. Some of these pages are filled manually, while others are generated automatically using classes and functions' docstrings to build technical documentation.

To generate technical documentation based on docstrings for a module, follow these steps:

1. **Create a Markdown File:**
   - Create a new Markdown file inside the `references/` folder (you can organize it further by placing it inside a subfolder, e.g., `references/python-lib/`).

2. **Add a Title:**
   - Add a title to your Markdown file to clearly indicate its content.

3. **Include the Module Documentation:**
   - Add the following line, replacing `<path_from_root_to_your_file>` with the path to the Python code you want to use as the documentation source:
   ```markdown
   ::: <path_from_root_to_your_file>
   ```

That's it! Your technical documentation will now be generated based on the specified module's docstrings.

To build and deploy the documentation, you can use a specific CI or run the following command:

```sh
poetry run mkdocs gh-deploy --force
```

This will create a branch named `gh-pages`, which you can then link to GitHub Pages.

For more detailed information, refer to the [official MkDocs documentation](https://www.mkdocs.org/).

## Shortcut using taskfile

Task is a task runner and build tool designed to be simpler and easier to use than tools like GNU Make. Written in Go, Task is a single binary with no other dependencies, making it straightforward to install and use without any complicated setup.

To use Task, you simply describe your build tasks in a YAML schema within a file called `taskfile.yml`.

### Installation

To install Task, follow the official [installation guide](https://taskfile.dev/installation/).

### Running tasks

To run a task, use the following command in your terminal:

```sh
task <task-name>
```

For example, to initialize your project, run:

```sh
task init
```

### Benefits of using taskfile

- **Simplicity**: Task provides a simple YAML-based configuration, making it easy to define and manage tasks.
- **No Dependencies**: Being a single binary with no dependencies, Task simplifies the setup process.
- **Consistency**: Using Task ensures that everyone on your team runs tasks in the same way, reducing the risk of errors and inconsistencies.

## Semantic Release

Semantic Release ensures that each commit is analyzed to determine the next version and create a changelog based on standardized commit messages.

### Configuration

Version Tracking: Semantic Release updates version numbers in the following files:
- python-lib/deep2tower/\_\_init\_\_.py
- plugin.json
- pyproject.toml

### Commit Guidelines

The version is determined by commit messages using specific tags:
- Major Releases: Triggered by commits with the `feat!` tag (new features).
- Minor Releases: Triggered by commits with the `feat` tag (new features).
- Patch Releases: Triggered by commits with the `fix` or `perf` tags (bug fixes or performance improvements).

Allowed Commit Tags:
add, rm, build, conf, config, cfg, ci, docs, feat, fix, perf, style, refactor, test, merge.

### How It Works

On each commit to the main branch, Semantic Release will:
- Bump the version based on commit tags.
- Update the CHANGELOG.md.
- Create a new release on GitHub with the updated version.

> [!IMPORTANT]
> **To ensure that Semantic Release works correctly, follow the conventional commit style when writing your commit messages.**
