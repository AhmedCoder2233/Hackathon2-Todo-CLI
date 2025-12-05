from datetime import date, time, datetime, timedelta, timezone
import pytest
from src.models.task import Task

def test_task_is_overdue_past_due_date():
    """
    Tests that a task with a past due date is marked as overdue.
    """
    # Define a specific point in time for the overdue check
    check_time = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    # Create a task due before the check_time
    past_due_date = date(2024, 12, 31) # A date clearly before check_time
    task = Task(title="Past Due Task", due_date=past_due_date, due_time=time(12,0,0))
    assert task.is_overdue(current_datetime=check_time) is True

def test_task_is_not_overdue_future_due_date():
    """
    Tests that a task with a future due date is not marked as overdue.
    """
    # Define a specific point in time for the overdue check
    check_time = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    # Create a task due after the check_time
    future_due_date = date(2025, 1, 2) # A date clearly after check_time
    task = Task(title="Future Due Task", due_date=future_due_date, due_time=time(12,0,0))
    assert task.is_overdue(current_datetime=check_time) is False

def test_task_is_overdue_past_due_datetime():
    """
    Tests that a task with a past due datetime is marked as overdue.
    """
    # Define a specific point in time for the overdue check
    check_time = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    # Create a task due before the check_time
    past_due_datetime = datetime(2025, 1, 1, 11, 0, 0, tzinfo=timezone.utc) # 1 hour before check_time
    task = Task(title="Past Due Task with Time", due_date=past_due_datetime.date(), due_time=past_due_datetime.time())
    assert task.is_overdue(current_datetime=check_time) is True

def test_task_is_not_overdue_future_due_datetime():
    """
    Tests that a task with a future due datetime is not marked as overdue.
    """
    # Define a specific point in time for the overdue check
    check_time = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    # Create a task due after the check_time
    future_due_datetime = datetime(2025, 1, 1, 13, 0, 0, tzinfo=timezone.utc) # 1 hour after check_time
    task = Task(title="Future Due Task with Time", due_date=future_due_datetime.date(), due_time=future_due_datetime.time())
    assert task.is_overdue(current_datetime=check_time) is False

def test_task_is_not_overdue_no_due_date():
    """
    Tests that a task without a due date is not marked as overdue.
    """
    task = Task(title="Task without Due Date")
    assert task.is_overdue() is False

def test_valid_due_date_and_time():
    """
    Tests that a task can be created with a valid future due date and time without errors.
    """
    future_date = date.today() + timedelta(days=1)
    valid_time = time(10, 30)
    try:
        task = Task(title="Valid Task", due_date=future_date, due_time=valid_time)
        assert task.due_date == future_date
        assert task.due_time == valid_time
    except ValueError as e:
        pytest.fail(f"Valid due date/time raised an unexpected error: {e}")

def test_fr009_future_due_date_no_error():
    """
    FR-009: Tests that creating a task with a future due date does not raise an error.
    """
    future_date = date.today() + timedelta(days=1)
    try:
        Task(title="Future Due Task", due_date=future_date)
    except ValueError as e:
        pytest.fail(f"Creating task with future due date raised an unexpected error: {e}")