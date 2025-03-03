# lvmh-ai-dataiku-plugin-retrieval-reco

This repository contains the deep2tower Dataiku plugin.

## Project layout

- <details open>
     <summary>:open_file_folder: Plugin directory</summary>
    - <details>
        <summary>:open_file_folder: `.github/` GitHub Actions and Workflows directory</summary>
        - <details>
            <summary>:open_file_folder: `actions/` GitHub Actions directory</summary>
            - :material-git: `action.yml` Setup Python and Poetry Action
        - <details>
            <summary>:open_file_folder: `workflows/` GitHub workflows directory</summary>
            - :material-git: `github-actions.yml` GitHub Action CI
            - :material-git: `mkdocs-build.yml` Build and deploy MkDocs to GitHub Pages
            - :material-git: `semantic-release.yml` Run Semantic Release
    - <details>
        <summary>:open_file_folder: `code-env/` DSS env configuration directory</summary>
        - <details>
            <summary>:open_file_folder: `spec/`</summary>
            - :material-file-document: `requirements.txt` DSS code env requirements
        - :simple-json: `desc.json` Code env configuration
    - <details>
         <summary>:open_file_folder: `custom-recipes/` DSS custom recipes directory</summary>
        - <details>
            <summary>:open_file_folder: `template-recipe` Custom recipe folder</summary>
            - :simple-python: `recipe.py` Recipe Python code
            - :simple-json: `recipe.json` Recipe front and parameters
    - <details>
        <summary>:open_file_folder: `docs/` Documentation directory</summary>
        - <details>
            <summary>:open_file_folder: `contributing` Base documentation folder</summary>
            - :material-language-markdown: `documentation.md` Mkdocs usage to build documentation
            - :material-language-markdown: `github-ci-cd.md` GitHub CI usage
            - :material-language-markdown: `installation.md` Plugin installation fo dev
            - :material-language-markdown: `pre-commit.md` Pre-commit usage
            - :material-language-markdown: `tasks.md` Tasks usage
        - <details>
            <summary>:open_file_folder: `references` Libraries references documentation folder</summary>
            - <details>
                <summary>:open_file_folder: `python-lib` Python-lib references folder</summary>
                - :material-language-markdown: `your_module.md` To reference for auto-documentation
            - :material-language-markdown: `python-lib.md` Describe the main lib
        - :material-language-markdown: `coding-style.md` Code best practices
        - :material-language-markdown: `index.md` Home for documentation
    - <details>
        <summary>:open_file_folder: `python-lib/` Library directory</summary>
        - <details>
            <summary>:open_file_folder: `src/` Source folder</summary>
            - <details>
                <summary>:open_file_folder: `bin/` Main functions folder</summary>
                - :simple-python: Python files
                - :octicons-file-16: Other Python files
            - <details>
                <summary>:open_file_folder: `lib/` Classes and functions folder</summary>
                - :simple-python: Python files
                - :octicons-file-16: Other Python files
            - <details>
                <summary>:open_file_folder: `utils/` Utilities folder</summary>
                - :simple-python: Python files
                - :octicons-file-16: Other Python files
        - <details>
            <summary>:open_file_folder: `tests/` Test folder</summary>
            - :simple-python: Python files
    - <details>
        <summary>:open_file_folder: `tasks/` Task files directory</summary>
        - :simple-task: `taskfile.hook.yaml` Tasks file for running git hooks
        - :simple-task: `taskfile.lock.yaml` Tasks file for running env export to dss env folder
        - :simple-task: `taskfile.serve.yaml` Tasks file for running mkdocs local server
        - :octicons-file-16: Other tasks files
    - :material-git: `.gitignore` Git ignore file
    - :material-file-cog: `.pre-commit-config.yaml` Pre commit hooks configuration file
    - :material-file-cog: `mkdocs.yml` MkDocs configuration file
    - :material-file-cog: `plugin.json` DSS plugin configuration file
    - :simple-poetry: `poetry.toml` Poetry configuration file
    - :simple-poetry: `pyproject.toml` Poetry project configuration file
    - :material-language-markdown: `README.md` README file
    - :simple-task: `taskfile.yaml` Main tasks file
</details>