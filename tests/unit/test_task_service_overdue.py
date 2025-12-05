from datetime import date, timedelta, datetime, time, timezone # Added datetime, time, timezone
import pytest
from src.models.task import Task
from src.services.task_service import TaskService

def test_get_overdue_tasks_returns_only_overdue():
    """
    Tests that get_overdue_tasks method correctly identifies and returns only overdue tasks.
    """
    service = TaskService()
    
    # Define a fixed point in time for the test to simulate "now" for overdue checks
    test_current_datetime = datetime.now(timezone.utc) + timedelta(days=5) # 5 days from now
    
    # Task due before test_current_datetime, but in the future relative to date.today()
    overdue_task_due_date = date.today() + timedelta(days=1) # Due 1 day from now
    overdue_task = service.add_task(title="Overdue Task", due_date=overdue_task_due_date, due_time=time(0, 0, 0))
    
    # Not overdue task (due in future relative to test_current_datetime)
    future_task_due_date = test_current_datetime.date() + timedelta(days=1) # Due 1 day after test_current_datetime
    future_task = service.add_task(title="Future Task", due_date=future_task_due_date, due_time=time(0, 0, 0))
    
    # Not overdue task (no due date)
    no_due_date_task = service.add_task(title="No Due Date Task")
    
    # Completed task (even if due in past, it's completed)
    completed_overdue_task_due_date = date.today() + timedelta(days=1)
    completed_overdue_task = service.add_task(title="Completed Overdue Task", due_date=completed_overdue_task_due_date, due_time=time(0, 0, 0), is_completed=True)

    overdue_tasks = service.get_overdue_tasks(current_datetime=test_current_datetime)

    assert len(overdue_tasks) == 1
    assert overdue_task in overdue_tasks
    assert future_task not in overdue_tasks
    assert no_due_date_task not in overdue_tasks
    assert completed_overdue_task not in overdue_tasks

def test_get_overdue_tasks_empty_when_no_overdue():
    """
    Tests that get_overdue_tasks returns an empty list when no tasks are overdue.
    """
    service = TaskService()
    
    today = date.today()
    tomorrow = today + timedelta(days=1)

    service.add_task(title="Future Task 1", due_date=tomorrow)
    service.add_task(title="Future Task 2", due_date=tomorrow)
    service.add_task(title="No Due Date Task")

    overdue_tasks = service.get_overdue_tasks()
    assert len(overdue_tasks) == 0
    assert overdue_tasks == []

def test_get_overdue_tasks_with_time_component():
    """
    Tests that get_overdue_tasks correctly handles tasks with time components for overdue detection.
    """
    from datetime import datetime, time, timezone

    service = TaskService()
    
    # Define a specific "current time" for the overdue check
    # Let the check_time be 2 days from today, at noon UTC
    check_time_date = date.today() + timedelta(days=2)
    check_time = datetime.combine(check_time_date, time(12, 0, 0), tzinfo=timezone.utc)

    # Task due 1 hour before check_time (overdue)
    overdue_due_datetime = check_time - timedelta(hours=1)
    # This due_date will now be `date.today() + 2 days`, which is in the future.
    overdue_with_time_task = service.add_task(
        title="Overdue with Time", 
        due_date=overdue_due_datetime.date(), 
        due_time=overdue_due_datetime.time()
    )

    # Task due 1 hour after check_time (not overdue)
    future_due_datetime = check_time + timedelta(hours=1)
    future_with_time_task = service.add_task(
        title="Future with Time", 
        due_date=future_due_datetime.date(), 
        due_time=future_due_datetime.time()
    )

    overdue_tasks = service.get_overdue_tasks(current_datetime=check_time)
    assert len(overdue_tasks) == 1
    assert overdue_with_time_task in overdue_tasks
    assert future_with_time_task not in overdue_tasks

def test_get_overdue_tasks_excludes_completed():
    """
    Tests that get_overdue_tasks excludes tasks marked as completed, even if their due date is in the past.
    """
    service = TaskService()
    
    # Define a fixed point in time for the test to simulate "now" for overdue checks
    test_current_datetime = datetime.now(timezone.utc) + timedelta(days=5) # 5 days from now

    # Completed task, due before test_current_datetime, but added with a future date
    completed_overdue_task_due_date = date.today() + timedelta(days=1) # Due 1 day from now
    completed_overdue_task = service.add_task(title="Completed Past Due", due_date=completed_overdue_task_due_date, due_time=time(0, 0, 0), is_completed=True)
    
    overdue_tasks = service.get_overdue_tasks(current_datetime=test_current_datetime)
    assert len(overdue_tasks) == 0
    assert completed_overdue_task not in overdue_tasks
