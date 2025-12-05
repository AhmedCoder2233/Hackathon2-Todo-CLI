# Todo App Memory-Based Specification

A simple command-line interface (CLI) to-do application that manages tasks in-memory.

## Features

- Add tasks with title, priority, due date, optional due time, recurrence, and tags.
- List all tasks with their status, priority, tags, due date, due time, recurrence type, and overdue status.
- Update task details (title, priority, completion status, due date, due time, recurrence, reminder settings, tags).
- Define tasks that recur daily, weekly, or monthly, with automatic generation of the next instance upon completion.
- Set optional due times for tasks.
- Set reminders for tasks, with notifications triggered a specified number of minutes before the due time.
- Visually highlight tasks that are overdue.
- Manually process and trigger pending notifications.
- Delete tasks.
- Mark tasks as complete.
- Set task priority.
- Add tags to tasks.
- Search tasks by keyword in the title or description.
- Filter tasks by completion status, priority, tags, and due date range.
- Sort tasks by title, priority, or due date.

## Prerequisites

- Python 3.11+
- `uv` package manager

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd Hackathon2
    ```

2.  **Initialize the `uv` environment:**
    ```bash
    uv init
    ```

3.  **Install dependencies (if any):**
    ```bash
    uv add <package_name>
    ```
    *Note: Currently, there are no external dependencies for core functionality.*

## Usage

To run the application, execute the following command from the project root:

```bash
python -m src.cli.main
```

This will start the application in an interactive mode, presenting you with a menu of options to manage your to-do list.

### Menu Options

1.  **Add Task**: Create a new task with a title, description, priority, tags, optional due date, due time, recurrence type (Daily, Weekly, Monthly), and reminder minutes before due.
2.  **List All Tasks**: View all your current tasks, with filtering and sorting options. Tasks will show due dates/times, recurrence, and overdue status.
3.  **Update Task**: Change any detail of an existing task including title, description, completion status, priority, tags, due date, due time, recurrence, and reminder settings.
4.  **Mark Task as Complete**: Mark a task as done. For recurring tasks, this will trigger the creation of the next instance.
5.  **Delete Task**: Remove a task from your list.
6.  **Set Task Priority**: Change the priority of a task.
7.  **Add Tags to Task**: Add one or more tags to a task.
8.  **Search Tasks**: Find tasks by keywords in their title or description.
9.  **Process Notifications**: Manually trigger any pending notifications.
10. **Exit**: Quit the application.

## Running Tests

To run the unit tests, navigate to the project root and execute:

```bash
pytest
```
