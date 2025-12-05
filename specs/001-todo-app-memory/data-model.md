# Data Model for Todo App Memory-Based Specification

This document outlines the data model for the Todo App. The primary entity is the `Task`.

## Task Entity

A `Task` represents a single to-do item.

### Attributes

- **id** (string, required): A unique identifier for the task. This will be a UUID.
- **title** (string, required): The description of the task.
- **completed** (boolean, required): The status of the task. Defaults to `false`.
- **priority** (string): The priority of the task. Can be one of "High", "Medium", or "Low". Defaults to "Medium".
- **tags** (list of strings): A list of tags associated with the task. Can be empty.
- **dueDate** (datetime): The due date and time for the task. Can be null.
- **isRecurring** (boolean): Whether the task is recurring. Defaults to `false`.
- **recurrenceRule** (string): The recurrence rule for the task. Can be one of "daily", "weekly", or "monthly". Only applicable if `isRecurring` is `true`.

### State Transitions

- A `Task` is created with a `completed` status of `false`.
- The `completed` status can be toggled between `true` and `false`.
- When a recurring task is marked as complete, a new task is created with the next due date based on the `recurrenceRule`.
