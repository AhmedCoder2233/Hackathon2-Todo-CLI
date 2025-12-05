# Data Model: Intermediate Task Features for Todo App

## Entity: Task

Represents a single item on the to-do list, extended with priority and tags.

### Attributes:

-   **`id`** (string): Unique identifier for the task.
    -   *Validation*: Must be unique, auto-generated.
-   **`title`** (string): A brief description of the task.
    -   *Validation*: Required, non-empty.
-   **`description`** (string, optional): A more detailed explanation of the task.
    -   *Validation*: Optional.
-   **`status`** (enum: "pending", "completed"): The current state of the task.
    -   *Validation*: Must be one of the specified enum values. Default: "pending".
-   **`due_date`** (date, optional): The target completion date for the task.
    -   *Validation*: Optional, valid date format.
-   **`priority`** (enum: "High", "Medium", "Low"): The importance level of the task.
    -   *Validation*: Must be one of "High", "Medium", "Low". Default: "Medium".
-   **`tags`** (list of strings, optional): A list of keywords or categories associated with the task.
    -   *Validation*: Optional, each tag is a non-empty string.

### Relationships:

-   No direct relationships with other entities are introduced by these intermediate features.
