# Quickstart Guide: Advanced Features to Todo App

This guide provides a brief overview of how to utilize the new advanced features – Recurring Tasks, Due Dates, and Reminders – within the Todo App.

## Prerequisites

*   The Todo App is installed and operational.
*   You are familiar with basic task creation and management.

## 1. Creating a Recurring Task

Recurring tasks automatically generate new instances upon completion, saving you the effort of re-creating routine items.

**How to create:**

1.  **Start Task Creation**: Begin creating a new task as you normally would.
2.  **Add Recurrence Type**: Look for an option to specify recurrence. You can typically choose from:
    *   `Daily`
    *   `Weekly`
    *   `Monthly`
3.  **Save Task**: Save the task. It will now appear in your list as a recurring item.

**Example Usage (Interactive CLI):**

1.  From the main menu, select `1. Add Task` or `3. Update Task`.
2.  When prompted for "recurrence type (Daily, Weekly, Monthly)", enter your desired type (e.g., `Daily`, `Weekly`, `Monthly`).
3.  Fill in other task details as prompted.

**After completion:**
When you mark a recurring task instance as complete, a new instance will automatically be generated with an updated due date based on its recurrence type (e.g., next day for daily, next week for weekly).

## 2. Setting Due Dates and Reminders

Set deadlines for your tasks and receive notifications to stay on track.

**How to set:**

1.  **Create/Edit Task**: When creating or editing a task, look for options to set a due date and an optional due time.
2.  **Specify Due Date**: Enter the date the task is due (e.g., `2025-12-31`). The system will validate that this date is in the future.
3.  **Specify Due Time (Optional)**: If needed, enter a specific time (e.g., `17:00` for 5:00 PM) in 24-hour format. The system will validate the format.
4.  **Set Reminder (Optional)**: Provide the number of minutes before the due date/time you wish to receive a notification (e.g., `30` for 30 minutes before).
5.  **Save Task**: Save the task with its due date and reminder settings.

**Example Usage (Interactive CLI):**

1.  From the main menu, select `1. Add Task` or `3. Update Task`.
2.  When prompted for "due date (YYYY-MM-DD)", enter the desired date.
3.  When prompted for "due time (HH:MM, 24-hour)", enter the desired time (optional).
4.  When prompted for "reminder minutes before due", enter the number of minutes (optional).
5.  Fill in other task details as prompted.

**Receiving Notifications:**
Notifications will be triggered via your browser or application at the specified reminder time.

## 3. Checking for Overdue Tasks

Tasks that have passed their due date/time will be visually highlighted.

**How to check:**

1.  **View Task List**: Simply view your list of tasks.
2.  **Identify Overdue**: Overdue tasks will be clearly distinguished (e.g., in red text, with an "OVERDUE" label).

**Example Usage (Interactive CLI):**

1.  From the main menu, select `2. List All Tasks`.
2.  Overdue tasks will be clearly marked with `[OVERDUE]`.
