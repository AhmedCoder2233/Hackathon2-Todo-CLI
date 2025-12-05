import pytest
from datetime import datetime, timedelta, date, time, timezone
from src.models.task import Task
from src.models.notification import Notification
from src.services.task_service import TaskService
from src.services.notification_service import NotificationService

# Helper to advance time in tests
@pytest.fixture
def fixed_datetime_utc():
    """Fixture to provide a fixed UTC datetime for testing."""
    return datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

def test_overdue_task_integration(fixed_datetime_utc):
    """
    Tests the integration of TaskService overdue logic with a task lifecycle.
    """
    task_service = TaskService()
    
    # Create a task that will be due in the past relative to fixed_datetime_utc
    # but in the future relative to the *actual* date.today() to pass add_task validation.
    # For a robust test, we need a due_date that is older than fixed_datetime_utc.
    # We will ensure this by setting a due_date a few days from fixed_datetime_utc.
    # Then, when we check is_overdue with fixed_datetime_utc, it will be overdue.

    # Calculate a due_date that is in the future relative to current date,
    # but in the past relative to a hypothetical 'now' we'll use for checking overdue status.
    # Let's say today is Nov 1st, 2025. fixed_datetime_utc is Jan 1st, 2025.
    # This implies fixed_datetime_utc is actually in the *past*.
    # So, we should use fixed_datetime_utc as the reference point for "now" for test logic.
    # To bypass `ValueError: Due date cannot be in the past.`, we must ensure the `due_date` passed to `add_task`
    # is greater than `date.today()` *at the moment the test runs*.

    # For overdue tasks, let's make the task due *before* fixed_datetime_utc.
    # And to avoid the ValueError, let's make sure fixed_datetime_utc itself is a future date.
    # The fixture fixed_datetime_utc is 2025-01-01 12:00:00 UTC. If current date is Dec 4, 2025,
    # then fixed_datetime_utc is in the past. This means the ValueError will still trigger.

    # A better approach is to mock `date.today()` during the add_task call within the test.
    # Alternatively, ensure the due_date used to create the task is ALWAYS in the future
    # *relative to the test execution date*, and then pass a `current_datetime`
    # to `get_overdue_tasks` and `task.is_overdue` that makes the task appear overdue.

    # Let's use `fixed_datetime_utc` as our "mock current time" for checking overdue status.
    # The task's due date must be *before* this `fixed_datetime_utc`.
    # To pass `add_task` validation, we need to pick a `due_date` that is in the future.
    # This is getting complicated without `freezegun`.

    # Simpler fix: Make the task due slightly *after* the `fixed_datetime_utc`,
    # but when checking `is_overdue` we provide a `current_datetime` that is *after* the task's due date.

    task_due_datetime = fixed_datetime_utc - timedelta(hours=2) # Task due 2 hours before fixed_datetime_utc
    
    # Ensure this task_due_datetime's date component is in the future relative to current date,
    # or at least not hitting the ValueError in add_task.
    # For now, let's assume `fixed_datetime_utc` is a date that can be used for due_date without error.
    # (If `fixed_datetime_utc.date()` is in the past, it will still trigger the ValueError from add_task).
    # To correctly test this, we should make the task due date always in the future relative to execution time.
    # For example, by using `date.today() + timedelta(days=X)`
    # Let's revise the approach to always create tasks in the "future" relative to test run,
    # and then simulate 'now' for overdue checks.

    # Let the task be due a few days from now, but before our `fixed_datetime_utc` which acts as our 'present'
    # This requires `fixed_datetime_utc` to be sufficiently in the future.
    # As `fixed_datetime_utc` is 2025-01-01, if today is Dec 4, 2025, this is not in the future.
    # The fixed_datetime_utc fixture itself is problematic for this validation.

    # Let's assume `fixed_datetime_utc` represents the 'present' moment for the test.
    # We will create a task that is due 'before' this present moment.
    # To avoid the `ValueError` from `add_task`, we need to ensure the due_date is >= `date.today()`
    # at the time the test is executed.

    # To simplify, we will create a task with `due_date` that is `date.today() + 1 day`
    # and then use `current_datetime` in `is_overdue` that is `date.today() + 2 days`
    # This way, the task is successfully added, but appears overdue when checked.

    # This requires modifying the fixed_datetime_utc fixture to be a more dynamic "now" for the test.
    # For now, let's assume fixed_datetime_utc is a valid "future" reference point from add_task perspective.
    # The error `ValueError: Due date cannot be in the past.` in the test output means `fixed_datetime_utc.date()`
    # itself is in the past relative to the test runner's `date.today()`.
    
    # To fix this, we'll make the due date a future date relative to the test run,
    # and *then* set a current_datetime to make it overdue.

    # Task is due 1 day from today.
    task_due_date = date.today() + timedelta(days=1)
    task_due_time = time(10, 0, 0) # Arbitrary time

    # Our "current time" for checking overdue will be 2 days from today, after task_due_date.
    simulated_overdue_check_time = datetime.combine(date.today() + timedelta(days=2), time(0, 0, 0), tzinfo=timezone.utc)

    overdue_task = task_service.add_task(
        title="Integration Overdue Task",
        due_date=task_due_date,
        due_time=task_due_time,
        description="This task should be overdue."
    )

    # Check if the task is correctly identified as overdue using our simulated time
    retrieved_overdue_tasks = task_service.get_overdue_tasks(current_datetime=simulated_overdue_check_time)
    assert len(retrieved_overdue_tasks) == 1
    assert retrieved_overdue_tasks[0].id == overdue_task.id
    assert retrieved_overdue_tasks[0].is_overdue(current_datetime=simulated_overdue_check_time) is True

    # Mark task as completed - it should no longer be overdue
    task_service.update_task(overdue_task.id, is_completed=True)
    retrieved_overdue_tasks_after_completion = task_service.get_overdue_tasks(current_datetime=simulated_overdue_check_time)
    assert len(retrieved_overdue_tasks_after_completion) == 0
    assert task_service.get_task(overdue_task.id).is_overdue(current_datetime=simulated_overdue_check_time) is False
def test_reminder_trigger_integration(fixed_datetime_utc):
    """
    Tests the integration of TaskService and NotificationService for reminders.
    """
    task_service = TaskService()
    notification_service = NotificationService()

    # Create a task with a due date in the future relative to date.today()
    # Let's set the due date to be 2 days from today, and time to be 10:00 AM UTC
    task_due_date = date.today() + timedelta(days=2)
    task_due_time = time(10, 0, 0)
    
    # The reminder should trigger some minutes before that
    reminder_minutes_before_due = 30
    
    task_with_reminder = task_service.add_task(
        title="Reminder Test Task",
        due_date=task_due_date,
        due_time=task_due_time,
        reminder_minutes_before_due=reminder_minutes_before_due
    )

    # Now, we need to define our "simulated current time" for checking notifications.
    # The task will be due at `task_due_datetime`.
    task_due_datetime_full = datetime.combine(task_due_date, task_due_time, tzinfo=timezone.utc)
    expected_trigger_time = task_due_datetime_full - timedelta(minutes=reminder_minutes_before_due)

    # Let's verify schedule_reminder behavior
    notification = notification_service.schedule_reminder(task_with_reminder)
    assert notification is not None
    assert notification.trigger_time == expected_trigger_time

    # Simulate time passing to *before* the trigger time
    # This simulated_current_time should be slightly before expected_trigger_time
    simulated_before_trigger_time = expected_trigger_time - timedelta(minutes=1)
    pending_before_trigger = notification_service.get_pending_notifications(simulated_before_trigger_time)
    assert notification not in pending_before_trigger # Should not be pending yet
    assert len(pending_before_trigger) == 0

    # Simulate time passing to just *at or past* the trigger time
    simulated_at_trigger_time = expected_trigger_time + timedelta(seconds=1) # 1 second past trigger
    
    # Assert that the notification becomes pending
    pending_after_trigger = notification_service.get_pending_notifications(simulated_at_trigger_time)
    assert len(pending_after_trigger) == 1
    assert pending_after_trigger[0].id == notification.id

    # Simulate triggering the notification (as NotificationManager would do)
    notification_service.mark_notification_delivered(notification.id)
    
    # Assert notification is delivered and no longer pending
    delivered_notification = notification_service.get_notification(notification.id)
    assert delivered_notification.is_delivered is True
    assert len(notification_service.get_pending_notifications(simulated_at_trigger_time)) == 0

