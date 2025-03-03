# Mkdocs usage to build documentation

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
