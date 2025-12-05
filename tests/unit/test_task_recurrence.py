import pytest
from datetime import date, timedelta
from src.models.task import Task
from src.lib.recurrence_util import get_next_recurrence_date # This utility will be implemented later in T017



# Test cases for Task model's recurrence logic
def test_task_get_next_recurrence_date_daily():
    today = date.today()
    task = Task(title="Daily chore", due_date=today, recurrence_type="Daily")
    # Assuming the Task model will eventually use get_next_recurrence_date
    next_date = get_next_recurrence_date(task.due_date, task.recurrence_type)
    assert next_date == today + timedelta(days=1)

def test_task_get_next_recurrence_date_weekly():
    today = date.today()
    task = Task(title="Weekly meeting", due_date=today, recurrence_type="Weekly")
    next_date = get_next_recurrence_date(task.due_date, task.recurrence_type)
    assert next_date == today + timedelta(weeks=1)

def test_task_get_next_recurrence_date_monthly():
    today = date(2025, 1, 15) # Use a fixed date for predictable monthly test
    task = Task(title="Monthly bill", due_date=today, recurrence_type="Monthly")
    next_date = get_next_recurrence_date(task.due_date, task.recurrence_type)
    assert next_date == date(2025, 2, 15)

    today = date(2025, 1, 31) # Test month end
    task = Task(title="Monthly report", due_date=today, recurrence_type="Monthly")
    next_date = get_next_recurrence_date(task.due_date, task.recurrence_type)
    assert next_date == date(2025, 2, 28) # February has 28 days

def test_task_get_next_recurrence_date_unsupported_type():
    today = date.today()
    task = Task(title="One-off task", due_date=today, recurrence_type="Unsupported")
    with pytest.raises(ValueError, match="Unsupported recurrence type"):
        get_next_recurrence_date(task.due_date, task.recurrence_type)
