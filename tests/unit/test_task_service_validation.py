from datetime import date, time, timedelta
import pytest
from src.services.task_service import TaskService
from src.models.task import Task

@pytest.fixture
def task_service_with_validation():
    """Provides a fresh TaskService instance for each test."""
    return TaskService()

def test_add_task_fr009_past_due_date_raises_error(task_service_with_validation):
    """
    FR-009: Tests that adding a task with a past due date raises a ValueError in TaskService.
    """
    past_date = date.today() - timedelta(days=1)
    with pytest.raises(ValueError, match="Due date cannot be in the past."):
        task_service_with_validation.add_task(title="Invalid Past Due Task", due_date=past_date)

def test_add_task_fr010_invalid_due_time_raises_error(task_service_with_validation):
    """
    FR-010: Tests that adding a task with an invalid due time type raises a ValueError in TaskService.
    Task model expects a datetime.time object, so passing a string should raise an error.
    """
    with pytest.raises(ValueError, match="Due time must be a valid time object \(HH:MM\)."):
        task_service_with_validation.add_task(title="Invalid Due Time Task", due_date=date.today(), due_time="25:00") # Pass string

def test_add_task_valid_due_date_and_time(task_service_with_validation):
    """
    Tests that a task can be added with a valid future due date and time without errors.
    """
    future_date = date.today() + timedelta(days=1)
    valid_time = time(10, 30)
    try:
        task = task_service_with_validation.add_task(title="Valid Task", due_date=future_date, due_time=valid_time)
        assert task.due_date == future_date
        assert task.due_time == valid_time
    except ValueError as e:
        pytest.fail(f"Valid due date/time raised an unexpected error: {e}")

def test_update_task_fr009_past_due_date_raises_error(task_service_with_validation):
    """
    FR-009: Tests that updating a task with a past due date raises a ValueError in TaskService.
    """
    task = task_service_with_validation.add_task(title="Existing Task", due_date=date.today() + timedelta(days=5))
    past_date = date.today() - timedelta(days=1)
    with pytest.raises(ValueError, match="Due date cannot be in the past."):
        task_service_with_validation.update_task(task.id, due_date=past_date)

def test_update_task_fr010_invalid_due_time_raises_error(task_service_with_validation):
    """
    FR-010: Tests that updating a task with an invalid due time type raises a ValueError in TaskService.
    """
    task = task_service_with_validation.add_task(title="Existing Task", due_date=date.today() + timedelta(days=5), due_time=time(10,0))
    with pytest.raises(ValueError, match="Due time must be a valid time object \(HH:MM\)."):
        task_service_with_validation.update_task(task.id, due_time="invalid_time") # Pass string

def test_update_task_valid_due_date_and_time(task_service_with_validation):
    """
    Tests that a task can be updated with a valid future due date and time without errors.
    """
    task = task_service_with_validation.add_task(title="Existing Task")
    future_date = date.today() + timedelta(days=1)
    valid_time = time(10, 30)
    try:
        updated_task = task_service_with_validation.update_task(task.id, due_date=future_date, due_time=valid_time)
        assert updated_task.due_date == future_date
        assert updated_task.due_time == valid_time
    except ValueError as e:
        pytest.fail(f"Valid due date/time update raised an unexpected error: {e}")
