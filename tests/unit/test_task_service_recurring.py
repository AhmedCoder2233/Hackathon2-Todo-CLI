import pytest
from datetime import date, time, timedelta
from unittest.mock import MagicMock
from src.models.task import Task
from src.services.task_service import TaskService

@pytest.fixture
def mock_task_repository():
    repo = MagicMock()
    repo.get_all.return_value = []
    repo.get_by_id.side_effect = lambda task_id: {}.get(task_id) # Simulate no task found by default
    repo.add.return_value = None
    repo.update.return_value = None
    repo.delete.return_value = None
    return repo

@pytest.fixture
def task_service(mock_task_repository):
    service = TaskService()
    service._tasks = {} # Ensure a clean state for in-memory storage
    return service

def test_create_recurring_task_daily(task_service):
    title = "Daily Standup"
    due_date = date.today() + timedelta(days=1)
    recurrence_type = "Daily"

    # Assume TaskService.add_task will correctly handle the recurrence_type
    task = task_service.add_task(title=title, due_date=due_date, recurrence_type=recurrence_type)

    assert task is not None
    assert task.title == title
    assert task.due_date == due_date
    assert task.recurrence_type == recurrence_type
    assert task.is_completed == False

    # Verify the task is added to the service's internal storage
    retrieved_task = task_service.get_task(task.id)
    assert retrieved_task == task

def test_create_recurring_task_weekly(task_service):
    title = "Weekly Review"
    due_date = date.today() + timedelta(weeks=1)
    recurrence_type = "Weekly"

    task = task_service.add_task(title=title, due_date=due_date, recurrence_type=recurrence_type)

    assert task.recurrence_type == recurrence_type
    assert task.due_date == due_date

def test_create_recurring_task_monthly(task_service):
    title = "Monthly Report"
    due_date = date(date.today().year, date.today().month, 1) + timedelta(days=30) # Approx next month
    recurrence_type = "Monthly"

    task = task_service.add_task(title=title, due_date=due_date, recurrence_type=recurrence_type)

    assert task.recurrence_type == recurrence_type
    assert task.due_date == due_date

def test_create_recurring_task_with_reminder(task_service):
    title = "Meeting with Client"
    due_date = date.today() + timedelta(days=2)
    due_time = time(10, 0)
    reminder_minutes = 60
    recurrence_type = "Daily"

    task = task_service.add_task(
        title=title,
        due_date=due_date,
        due_time=due_time,
        recurrence_type=recurrence_type,
        reminder_minutes_before_due=reminder_minutes
    )

    assert task.due_time == due_time
    assert task.reminder_minutes_before_due == reminder_minutes

def test_handle_task_completion_generates_next_instance(task_service):
    # Setup: Create a recurring task instance
    original_due_date = date.today()
    original_task = task_service.add_task(
        title="Daily chore",
        due_date=original_due_date,
        recurrence_type="Daily",
        description="Do daily cleanup"
    )
    # Simulate marking the task as complete
    task_service.update_task(original_task.id, is_completed=True)

    # Expected behavior: a new task should be added with the next due date
    next_due_date = original_due_date + timedelta(days=1)
    
    # After update_task completes the original_task, it should have generated a new task.
    # Let's search for a task with original_recurring_task_id set to original_task.id
    generated_tasks = [task for task in task_service.get_all_tasks() 
                       if task.original_recurring_task_id == original_task.id and 
                          task.due_date == next_due_date]

    assert len(generated_tasks) == 1
    generated_task = generated_tasks[0]
    
    assert generated_task is not None
    assert generated_task.title == "Daily chore"
    assert generated_task.due_date == next_due_date
    assert generated_task.recurrence_type == "Daily"
    assert generated_task.original_recurring_task_id == original_task.id
    assert not generated_task.is_completed

def test_prevent_duplicate_recurring_instances(task_service):
    # Setup: Create a recurring task for tomorrow
    today = date.today()
    tomorrow = today + timedelta(days=1)
    task_service.add_task(
        title="Daily reminder",
        due_date=tomorrow,
        recurrence_type="Daily",
        original_recurring_task_id="parent-task-id"
    )

    # Attempt to add another recurring task for the same title, due date, and recurrence type
    # The create_recurring_task method in TaskService already has duplicate checking logic.
    with pytest.raises(ValueError, match="A recurring task with the same title, due date, and recurrence type already exists and is not completed."):
        task_service.create_recurring_task(
            title="Daily reminder",
            due_date=tomorrow,
            recurrence_type="Daily",
            # original_recurring_task_id is not directly part of the duplicate check in create_recurring_task for now
        )
