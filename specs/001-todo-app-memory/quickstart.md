# Quickstart for Todo App Memory-Based Specification

This guide provides instructions for setting up and running the Todo App.

## Prerequisites

- Python 3.11
- `uv` package manager
- WSL (Windows Subsystem for Linux)

## Setup

1.  **Initialize the `uv` environment:**
    ```bash
    uv init
    ```

2.  **Install dependencies (if any):**
    ```bash
    uv add <package_name>
    ```
    *Note: Currently, there are no external dependencies.*

## Running the Application

The application is a command-line interface (CLI) tool.

```bash
python src/cli/main.py <command> [options]
```

### Commands

- `add --title "My new task"`: Adds a new task.
- `list`: Lists all tasks.
- `update --id <task_id> --title "My updated task"`: Updates a task.
- `delete --id <task_id>`: Deletes a task.
- `complete --id <task_id>`: Marks a task as complete.

## Running Tests

To run the unit tests, use `pytest`:

```bash
pytest
```
