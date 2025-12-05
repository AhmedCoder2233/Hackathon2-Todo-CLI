import pytest
from datetime import date, timedelta
from src.services.task_service import TaskService
from src.models.task import Task # For direct comparison

@pytest.fixture
def clean_task_service():
    # Provide a fresh TaskService for each test
    service = TaskService()
    service._tasks = {} # Ensure it's empty
    return service

def test_full_recurring_task_lifecycle_daily(clean_task_service):
    # 1. Create a daily recurring task
    title = "Daily Reminder"
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    # Simulating the creation of a recurring task
    initial_task = clean_task_service.add_task(
        title=title,
        due_date=tomorrow,
        recurrence_type="Daily"
    )
    
    assert initial_task.title == title
    assert initial_task.due_date == tomorrow
    assert initial_task.recurrence_type == "Daily"
    assert not initial_task.is_completed
    
    # 2. Mark the initial task as complete (this will trigger auto-generation)
    # This test will initially fail because mark_as_complete doesn't auto-generate yet (T018)
    # The expected behavior is that mark_as_complete internally calls a method
    # that generates the next instance.
    
    # We're testing the *integration* so we expect the service to handle it end-to-end.
    # For now, this test is set up to fail until T018 and T019 are implemented.
    
    updated_task = clean_task_service.update_task(initial_task.id, is_completed=True)
    assert updated_task.is_completed # Initial task should be marked complete
    
    # 3. Verify auto-generation of the next instance
    # This requires a way to find the generated task.
    # We'll assume the service will have a way to retrieve new tasks.
    
    # For now, we'll manually check the tasks in the service's internal storage
    # and expect a new task with the next due date and linked to the original.
    
    next_due_date = tomorrow + timedelta(days=1)
    
    # Filter to find the newly generated recurring task
    generated_tasks = [
        task for task in clean_task_service.get_all_tasks()
        if task.original_recurring_task_id == initial_task.id and task.due_date == next_due_date
    ]
    
    assert len(generated_tasks) == 1
    next_instance = generated_tasks[0]
    
    assert next_instance.title == title
    assert next_instance.due_date == next_due_date
    assert next_instance.recurrence_type == "Daily"
    assert next_instance.original_recurring_task_id == initial_task.id
    assert not next_instance.is_completed # New instance should not be completed
    
    # Further check to ensure the new task is distinct but related
    assert next_instance.id != initial_task.id