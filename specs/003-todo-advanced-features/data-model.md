# Data Model: Advanced Features to Todo App

## Entities

### 1. Task (Core Entity - Extension)

This entity represents a single item to be completed and will be extended to incorporate advanced features like recurrence and reminders.

*   **Attributes:**
    *   `id`: String (Unique identifier for the task, e.g., UUID)
    *   `title`: String (Descriptive name of the task)
    *   `description`: String (Optional, detailed description)
    *   `priority`: Enum (`Low`, `Medium`, `High`) - *Assumed to be part of the existing model or to be added.*
    *   `tags`: List of Strings (Optional, keywords for categorization) - *Assumed to be part of the existing model or to be added.*
    *   `is_completed`: Boolean (True if the task is finished, False otherwise)
    *   `created_at`: Datetime (UTC, timestamp of task creation)
    *   `updated_at`: Datetime (UTC, timestamp of last modification)

    *   **New Attributes for Advanced Features:**
        *   `due_date`: Date (Required for tasks with reminders, stored in UTC)
        *   `due_time`: Time (Optional, 24-hour format HH:MM, stored in UTC. If `due_time` is not set, `due_date` typically defaults to end-of-day or a reasonable default for reminder calculation.)
        *   `recurrence_type`: Enum (`None`, `Daily`, `Weekly`, `Monthly`) - Default `None`
        *   `reminder_minutes_before_due`: Integer (Optional, number of minutes before `due_date` + `due_time` to trigger a reminder. Default to system-defined value if not set.)
        *   `original_recurring_task_id`: String (Optional, reference to the parent recurring task if this is a generated instance) - *Useful for tracking recurring series.*

*   **Validation Rules (from Functional Requirements):**
    *   `due_date` MUST not be in the past when creating or updating (FR-009).
    *   `due_time` MUST be in a valid 24-hour format (HH:MM) if provided (FR-010).

*   **State Transitions:**
    *   When `is_completed` is set to `True` for a task with `recurrence_type` not `None`, a new `Task` instance is automatically generated based on the recurrence rules (FR-002).

### 2. Notification (New Entity)

This entity represents a scheduled or triggered alert for a task reminder.

*   **Attributes:**
    *   `id`: String (Unique identifier for the notification, e.g., UUID)
    *   `message`: String (Content of the notification, derived from the task)
    *   `trigger_time`: Datetime (UTC, the exact time the notification should be displayed/pushed)
    *   `task_id`: String (Foreign Key, reference to the `Task` that this notification is for)
    *   `is_delivered`: Boolean (Indicates if the notification has been successfully delivered/displayed)
    *   `delivered_at`: Datetime (UTC, timestamp of when the notification was delivered, if applicable)

## Relationships

*   **Task to Notification**: One-to-Many (`1:N`)
    *   A single `Task` (especially a recurring one or one with multiple reminders) can be associated with multiple `Notification` instances. Each `Notification` directly references the `Task` it pertains to via `task_id`.
