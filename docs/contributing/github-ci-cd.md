# GitHub Actions

GitHub Actions is a robust Continuous Integration/Continuous Development (CI/CD) tool provided by GitHub. It automates workflows by allowing you to build, test, and deploy your code directly from your GitHub repository. For more detailed information, see the [official documentation](https://docs.github.com/en/actions).

For plugin development, we utilize CI/CD to enforce code quality standards and streamline the release process. Our CI pipeline ensures that every merge request passes through a series of checks, including:
- Linters and Formatters: We run Ruff for both linting and formatting to maintain a consistent and clean codebase.
- Docstring Validation: We use Interrogate to verify that the code is properly documented with required docstrings.
- Unit Tests: Comprehensive unit tests are executed to ensure no regressions or functional issues are introduced.

In addition to these quality checks, we automate our release process using Semantic Release. This system manages versioning, updates tags, generates the CHANGELOG, and creates new releases based on commit messages, making the release process consistent and error-free.

Our CI/CD also handles documentation using MkDocs. It automatically builds and deploys the latest documentation to a dedicated `gh-pages` branch, ensuring it is continuously updated and accessible via GitHub Pages.

## Setup action

**Purpose**:
This is a reusable GitHub Action for setting up Python and Poetry in your CI/CD workflows. It defines inputs, such as Python and Poetry versions, and steps to install and configure them.

### Key Sections:
- **Inputs**:
  - `python-version`: Specifies the Python version to use (default: `3.9`).
  - `poetry-version`: Specifies the Poetry version to use (default: `1.8.3`).
  - `poetry-args`: Allows additional arguments to be passed to Poetry.
  - `load-cache`: Defines whether to load a cached virtual environment (default: `true`).

- **Steps**:
  1. **Set up Python**: Installs and sets up the specified version of Python.
  2. **Install Poetry**: Installs the specified version of Poetry.
  3. **Load cached venv**: Attempts to load the cached virtual environment, speeding up dependency installation.
  4. **Install dependencies**: If the cache is not hit, it installs the dependencies using Poetry with any provided arguments.

**Usage**: This action is reused in other workflows to set up the necessary environment for running Python and Poetry-based projects.

## Main action

**Purpose**:
This workflow runs various quality checks and tests on every pull request to ensure code quality before merging. It includes steps to run linters, formatters, docstring validation, and unit tests.

### Key Sections:
- **Triggers**:
  - Runs on pull requests targeting the `main` or `dev` branches.

- **Job Configuration**:
  - **Runs-on**: Specifies the `ubuntu-latest` environment for running the CI pipeline.
  - **Matrix**: Defines a matrix strategy to test with different versions of Python (`3.9`) and Poetry (`1.8.3`).

- **Steps**:
  1. **Check-out repository**: Fetches the code repository.
  2. **Setup Workflow**: Uses the custom `.github/actions/setup` action to set up Python and Poetry.
  3. **Run Ruff linter**: Runs Ruff to check code quality without modifying the code.
  4. **Run Ruff formatter**: Runs Ruff to check and enforce code formatting.
  5. **Run Interrogate**: Runs Interrogate to check for missing docstrings.
  6. **Run unit tests**: Runs unit tests using Pytest to ensure functionality.

## MkDocs build

**Purpose**:
This workflow automatically builds and deploys MkDocs-based documentation to GitHub Pages when relevant changes are made to the documentation.

### Key Sections:
- **Triggers**:
  - Runs when the `Run Semantic Release` workflow completes successfully.

- **Permissions**:
  - Grants write access to the contents to publish the built documentation.

- **Job Configuration**:
  - **Runs-on**: Specifies `ubuntu-latest`.
  - **Matrix**: Tests with Python `3.9` and Poetry `1.8.3`.

- **Steps**:
  1. **Check-out repository**: Fetches the code repository.
  2. **Setup Workflow**: Uses the custom `.github/actions/setup` action to set up Python and Poetry.
  3. **Configure Git credentials**: Configures Git credentials using GitHub's default bot user for pushing changes to the repository.
  4. **Build and deploy MkDocs**: Builds the MkDocs documentation and deploys it to the `gh-pages` branch, making it available on GitHub Pages.

## Semantic Release

**Purpose**:
This workflow automates versioning and the release process using Semantic Release. It manages tags, updates the CHANGELOG, and publishes new releases based on commit messages.

### Key Sections:
- **Triggers**:
  - Runs when a push is made to the `main` branch.

- **Permissions**:
  - Grants write access to the contents and the GitHub ID token for managing the release.

- **Job Configuration**:
  - **Runs-on**: Specifies `ubuntu-latest`.
  - **Matrix**: Tests with Python `3.9` and Poetry `1.8.3`.
  - **Concurrency**: Ensures that only one release job runs at a time.

- **Steps**:
  1. **Check-out repository**: Fetches the entire code repository (all branches and tags).
  2. **Setup Workflow**: Uses the custom `.github/actions/setup` action to set up Python and Poetry.
  3. **Run Semantic Release**: Executes Semantic Release to manage versioning and generate a new release.
  4. **Publish**: Publishes package distributions to GitHub Releases.
