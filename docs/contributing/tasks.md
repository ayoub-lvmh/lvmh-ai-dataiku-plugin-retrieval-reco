# Shortcut using taskfile

Task is a task runner and build tool designed to be simpler and easier to use than tools like GNU Make. Written in Go, Task is a single binary with no other dependencies, making it straightforward to install and use without any complicated setup.

To use Task, you simply describe your build tasks in a YAML schema within a file called `taskfile.yml`.

## Installation

To install Task, follow the official [installation guide](https://taskfile.dev/installation/).


## Running tasks

To run a task, use the following command in your terminal:

```sh
task <task-name>
```

For example, to initialize your project, run:

```sh
task init
```

## Benefits of using taskfile

- **Simplicity**: Task provides a simple YAML-based configuration, making it easy to define and manage tasks.
- **No Dependencies**: Being a single binary with no dependencies, Task simplifies the setup process.
- **Consistency**: Using Task ensures that everyone on your team runs tasks in the same way, reducing the risk of errors and inconsistencies.
