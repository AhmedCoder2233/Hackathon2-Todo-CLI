# Quickstart Guide: Intermediate Task Features

This guide provides a quick overview of how to interact with the new intermediate task features (priorities, tags, search, filter, and sort) in the Todo App CLI.

## Assigning Priorities and Tags

When creating or updating a task, you will be able to specify its priority and assign tags.

**Example (Conceptual CLI commands):**

```bash
# Create a new task with High priority and 'work', 'urgent' tags
todo add "Finish project report" --priority High --tags work,urgent --due 2025-12-10

# Update an existing task to Medium priority and add 'home' tag
todo update <task_id> --priority Medium --add-tag home
```

## Searching and Filtering Tasks

You can search for tasks by keywords in their title or description, and filter by various criteria.

**Example (Conceptual CLI commands):**

```bash
# Search for tasks containing "report"
todo search report

# Filter tasks by pending status and High priority
todo list --status pending --priority High

# Filter tasks by 'work' tag and due date within a range
todo list --tag work --due-before 2025-12-15 --due-after 2025-12-08
```

## Sorting Tasks

The task list can be sorted by due date, priority, or alphabetically.

**Example (Conceptual CLI commands):**

```bash
# Sort tasks by due date (ascending)
todo list --sort due_date asc

# Sort tasks by priority
todo list --sort priority

# Sort tasks alphabetically by title (descending)
todo list --sort title desc
```

## Default Priority Display

By default, tasks will be listed with High priority items first. This default is overridden if you apply any custom sorting.

*(Note: The exact CLI commands will be defined during the implementation phase.)*
