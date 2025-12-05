import pytest
from datetime import date, time, datetime, timedelta
from unittest.mock import MagicMock
from src.models.task import Task  # Will be updated in T006
from src.services.task_service import TaskService # Existing service


# Mock Task class for testing TaskService interactions
class MockTask:
    def __init__(self, id, title, is_completed=False, due_date=None, due_time=None,
                 recurrence_type=None, reminder_minutes_before_due=None, original_recurring_task_id=None):
        self.id = id
        self.title = title
        self.is_completed = is_completed
        self.due_date = due_date
        self.due_time = due_time
        self.recurrence_type = recurrence_type
        self.reminder_minutes_before_due = reminder_minutes_before_due
        self.original_recurring_task_id = original_recurring_task_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "is_completed": self.is_completed,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "due_time": self.due_time.isoformat() if self.due_time else None,
            "recurrence_type": self.recurrence_type,
            "reminder_minutes_before_due": self.reminder_minutes_before_due,
            "original_recurring_task_id": self.original_recurring_task_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

@pytest.fixture
def mock_task_repository():
    # Mock for the internal storage/repository of tasks within TaskService
    repo = MagicMock()
    repo.get_all.return_value = []
    repo.get_by_id.return_value = None
    repo.add.return_value = None
    repo.update.return_value = None
    repo.delete.return_value = None
    return repo

@pytest.fixture
def task_service():
    # Instantiate TaskService directly, as it manages tasks in-memory
    service = TaskService()
    return service

def test_task_service_can_handle_new_task_attributes(task_service):
    # This test verifies that TaskService methods can accept and store/retrieve
    # tasks with the new attributes.

    # Note: TaskService.add_task does not take 'id', it generates one.
    new_task_title = "Buy Groceries"
    due_date_val = date(2025, 12, 25)
    due_time_val = time(18, 0)
    recurrence_type_val = "Weekly"
    reminder_val = 60

    # Test adding a task with new attributes
    added_task = task_service.add_task(
        new_task_title,
        due_date=due_date_val,
        due_time=due_time_val,
        recurrence_type=recurrence_type_val,
        reminder_minutes_before_due=reminder_val
    )
    
    # Retrieve the task using the generated ID
    retrieved_task = task_service.get_task(added_task.id)

    assert retrieved_task is not None
    assert retrieved_task.title == new_task_title
    assert retrieved_task.due_date == due_date_val
    assert retrieved_task.due_time == due_time_val
    assert retrieved_task.recurrence_type == recurrence_type_val
    assert retrieved_task.reminder_minutes_before_due == reminder_val

    # Test updating a task with new attributes
    updated_title = "Buy More Groceries"
    
    updated_task = task_service.update_task(
        retrieved_task.id, # Use the generated ID for updating
        title=updated_title,
        due_date=date(2026, 1, 1),
        recurrence_type="Monthly"
    )

    assert updated_task is not None
    assert updated_task.title == updated_title
    assert updated_task.due_date == date(2026, 1, 1)
    assert updated_task.recurrence_type == "Monthly"
    assert updated_task.due_time == due_time_val # Should remain unchanged if not specified
    assert updated_task.reminder_minutes_before_due == reminder_val # Should remain unchanged
