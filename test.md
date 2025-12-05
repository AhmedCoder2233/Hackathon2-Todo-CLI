# To-Do Application Feature Tests

This document outlines example test cases to verify the functionality of the To-Do application's core features across Basic, Intermediate, and Advanced levels.

---

## Basic Level (Core Essentials)

### 1. Add Task
*   **Description**: Verify that a new task can be successfully added with a title and optional details.
*   **Steps**:
    1.  Start the CLI application.
    2.  Select option `1` (Add Task).
    3.  Enter "Buy groceries" as the title.
    4.  Enter "Milk, eggs, bread" as the description.
    5.  Enter "High" for priority.
    6.  Enter "home shopping" for tags.
    7.  Enter a future date (e.g., "YYYY-MM-DD") for due date.
    8.  Enter a future time (e.g., "HH:MM") for due time.
    9.  Enter "None" for recurrence.
    10. Enter `60` for reminder minutes.
    11. Confirm success message.
*   **Expected Result**: Task "Buy groceries" is added with all specified details.

### 2. View Task List
*   **Description**: Verify that all added tasks are displayed correctly.
*   **Steps**:
    1.  Add at least two tasks (e.g., "Buy groceries", "Call mom").
    2.  Select option `2` (List All Tasks).
    3.  Enter `n` for filters.
    4.  Enter `None` for sort.
*   **Expected Result**: Both "Buy groceries" and "Call mom" are displayed in the list.

### 3. Update Task
*   **Description**: Verify that an existing task's details can be modified.
*   **Steps**:
    1.  Add task "Meeting" (ID: XYZ).
    2.  Select option `3` (Update Task).
    3.  Enter ID: XYZ.
    4.  Change title to "Team Meeting".
    5.  Change priority to "High".
    6.  Confirm success message.
    7.  List all tasks.
*   **Expected Result**: Task with ID XYZ now shows title "Team Meeting" and priority "High".

### 4. Mark as Complete
*   **Description**: Verify that a task's completion status can be toggled.
*   **Steps**:
    1.  Add task "Draft report" (ID: ABC).
    2.  Select option `4` (Mark Task as Complete).
    3.  Enter ID: ABC.
    4.  Confirm success message.
    5.  List all tasks.
*   **Expected Result**: Task with ID ABC is displayed with a `✓` indicator.

### 5. Delete Task
*   **Description**: Verify that a task can be removed from the list.
*   **Steps**:
    1.  Add task "Old item" (ID: PQR).
    2.  Select option `5` (Delete Task).
    3.  Enter ID: PQR.
    4.  Confirm success message.
    5.  List all tasks.
*   **Expected Result**: Task with ID PQR is no longer in the list.

---

## Intermediate Level (Organization & Usability)

### 1. Set Task Priority
*   **Description**: Verify that a task's priority can be set or updated.
*   **Steps**:
    1.  Add task "Review document".
    2.  Select option `6` (Set Task Priority).
    3.  Enter the task's ID.
    4.  Enter "High" as the new priority.
    5.  Confirm success message.
    6.  List all tasks.
*   **Expected Result**: Task "Review document" shows priority "High" (e.g., with `🔴` emoji).

### 2. Add Tags to Task
*   **Description**: Verify that tags can be added to a task.
*   **Steps**:
    1.  Add task "Project X task".
    2.  Select option `7` (Add Tags to Task).
    3.  Enter the task's ID.
    4.  Enter "work important" as tags.
    5.  Confirm success message.
    6.  List all tasks.
*   **Expected Result**: Task "Project X task" is displayed with tags `(work, important)`.

### 3. Search Tasks
*   **Description**: Verify that tasks can be found by a keyword in their title or description.
*   **Steps**:
    1.  Add task "Buy milk" (description: "2% milk").
    2.  Add task "Walk dog" (description: "Walk in park").
    3.  Select option `8` (Search Tasks).
    4.  Enter keyword "milk".
*   **Expected Result**: Only "Buy milk" task is returned.

### 4. Filter Tasks
*   **Description**: Verify that tasks can be filtered by various criteria.
*   **Steps**:
    1.  Add three tasks:
        *   "High Priority Incomplete" (Priority: High, Completed: No, Due Date: Tomorrow)
        *   "Low Priority Complete" (Priority: Low, Completed: Yes, Due Date: Yesterday)
        *   "Medium Priority Incomplete" (Priority: Medium, Completed: No, Due Date: Day after tomorrow)
    2.  Select option `2` (List All Tasks).
    3.  Enter `y` for filters.
    4.  Filter by completed status `n`.
    5.  Filter by priority `High`.
    6.  Leave other filters blank.
*   **Expected Result**: Only "High Priority Incomplete" task is displayed.

### 5. Sort Tasks
*   **Description**: Verify that tasks can be sorted by title, priority, or due date.
*   **Steps**:
    1.  Add three tasks with different priorities and due dates:
        *   Task A (Due: Tomorrow, Priority: Medium)
        *   Task B (Due: Today, Priority: High)
        *   Task C (Due: Day after tomorrow, Priority: Low)
    2.  Select option `2` (List All Tasks).
    3.  Enter `n` for filters.
    4.  Enter `due_date` for sort.
*   **Expected Result**: Tasks are displayed in order: Task B (Today), Task A (Tomorrow), Task C (Day after tomorrow).

---

## Advanced Level (Intelligent Features)

### 1. Create Recurring Task
*   **Description**: Verify that a task can be set as recurring.
*   **Steps**:
    1.  Select option `1` (Add Task).
    2.  Enter "Daily meeting" as title.
    3.  Enter a future date for due date (e.g., tomorrow).
    4.  Enter "Daily" for recurrence type.
    5.  Confirm success message.
*   **Expected Result**: Task "Daily meeting" is added with `(Rec: Daily)` indicator.

### 2. Auto-generate Next Recurring Instance
*   **Description**: Verify that completing a recurring task generates its next instance.
*   **Steps**:
    1.  Add recurring task "Weekly report" (Due: next Monday, Recurrence: Weekly, ID: XYZ).
    2.  Select option `4` (Mark Task as Complete).
    3.  Enter ID: XYZ.
    4.  Confirm success message.
    5.  List all tasks.
*   **Expected Result**: The original task with ID XYZ is marked complete. A new task "Weekly report" appears with a due date of the Monday after next, and `original_recurring_task_id` matching XYZ.

### 3. Set Due Dates & Time Reminders
*   **Description**: Verify that a task can have a specific due date and time with a reminder.
*   **Steps**:
    1.  Select option `1` (Add Task).
    2.  Enter "Presentation prep".
    3.  Enter a future date (e.g., "YYYY-MM-DD") for due date.
    4.  Enter a future time (e.g., "HH:MM") for due time (e.g., 5 minutes from now).
    5.  Enter `3` for reminder minutes before due.
    6.  Confirm success message.
*   **Expected Result**: Task is added with specified due date, time, and reminder.

### 4. Console Notification Trigger
*   **Description**: Verify that reminders trigger console notifications when processed.
*   **Steps**:
    1.  Add task "Check email" with due date/time 2 minutes from now, reminder 1 minute before.
    2.  Wait for 1.5 minutes (past the reminder trigger time).
    3.  Select option `9` (Process Notifications).
*   **Expected Result**: A console message like "🔔 Notification: Reminder: 'Check email' is due soon! (Task ID: ...)" is displayed.

### 5. Overdue Status
*   **Description**: Verify that tasks past their due date/time are marked as overdue.
*   **Steps**:
    1.  Add task "Expired coupon" with a due date/time in the past (e.g., yesterday).
    2.  List all tasks.
*   **Expected Result**: Task "Expired coupon" is displayed with an `[OVERDUE]` indicator.
