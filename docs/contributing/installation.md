# Plugin installation

This guide provides step-by-step instructions for installing the plugin, including cloning the repository and initializing the project using Poetry for dependency management.

## Cloning the repository

To get started, you need to clone the repository to your local machine. Use the following command to clone the repository:

```sh
git clone <repository_url>
```

Replace `<repository_url>` with the actual URL of the repository.

## Poetry initialization

Poetry is a tool for dependency management and packaging in Python. It helps manage dependencies and virtual environments efficiently. With Poetry, you can also define and configure tools like Ruff and Interrogate. Note that Poetry is configured through the `pyproject.toml` file to create in-project virtual environments.

### Installing Poetry

If you don't have Poetry installed, you can install it by following the instructions on the [official Poetry installation page](https://python-poetry.org/docs/#installation).

### Basic commands for Poetry

1. **Install dependencies:**

   After cloning the repository, navigate to the project directory and run:

   ```sh
   poetry install
   ```

   This command will install all the dependencies listed in the `pyproject.toml` file and create a virtual environment based on the Poetry configuration in the `poetry.toml`.

2. **Activate the virtual environment:**

   To activate the virtual environment created by Poetry, use:

   ```sh
   poetry shell
   ```

   This command will activate the virtual environment so you can work within it.

3. **Add a new dependency:**

   If you need to add a new dependency to your project, run:

   ```sh
   poetry add <package_name>
   ```

   Replace `<package_name>` with the name of the package you want to add.

4. **Update dependencies:**

   To update the dependencies to their latest versions, use:

   ```sh
   poetry update
   ```

5. **Run scripts or commands within the virtual environment:**

   You can run any command within the virtual environment without activating it by prefixing it with `poetry run`. For example, to run tests using `pytest`, you can use:

   ```sh
   poetry run pytest
   ```

By following these steps, you can effectively manage your project's dependencies and virtual environment using Poetry.
