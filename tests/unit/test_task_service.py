import pytest
from src.services.task_service import TaskService

@pytest.fixture
def task_service():
    return TaskService()

def test_add_and_get_task(task_service: TaskService):
    task = task_service.add_task("Test Task")
    retrieved_task = task_service.get_task(task.id)
    assert retrieved_task is not None
    assert retrieved_task.title == "Test Task"

def test_get_all_tasks(task_service: TaskService):
    task1 = task_service.add_task("Test Task 1")
    task2 = task_service.add_task("Test Task 2")
    all_tasks = task_service.get_all_tasks()
    assert len(all_tasks) == 2
    assert task1 in all_tasks
    assert task2 in all_tasks

def test_update_task(task_service: TaskService):
    task = task_service.add_task("Original Title")
    updated_task = task_service.update_task(task.id, title="Updated Title", is_completed=True)
    assert updated_task is not None
    assert updated_task.title == "Updated Title"
    assert updated_task.is_completed is True

def test_update_nonexistent_task(task_service: TaskService):
    updated_task = task_service.update_task("nonexistent_id", title="New Title")
    assert updated_task is None

def test_delete_task(task_service: TaskService):
    task = task_service.add_task("Task to be deleted")
    assert task_service.delete_task(task.id) is True
    assert task_service.get_task(task.id) is None

def test_delete_nonexistent_task(task_service: TaskService):
    assert task_service.delete_task("nonexistent_id") is False

def test_complete_task(task_service: TaskService):
    task = task_service.add_task("Incomplete Task")
    completed_task = task_service.update_task(task.id, is_completed=True)
    assert completed_task is not None
    assert completed_task.is_completed is True

def test_set_priority(task_service: TaskService):
    task = task_service.add_task("Test Task")
    updated_task = task_service.update_task(task.id, priority="High")
    assert updated_task is not None
    assert updated_task.priority == "High"

def test_add_tags(task_service: TaskService):
    task = task_service.add_task("Test Task")
    updated_task = task_service.update_task(task.id, tags=["work", "urgent"])
    assert updated_task is not None
    assert updated_task.tags == ["work", "urgent"]

def test_search_tasks(task_service: TaskService):
    task_service.add_task("Buy milk", description="Remember to get whole milk.")
    task_service.add_task("Walk the dog", description="Take him to the park.")
    
    # Search by title
    results = task_service.search_tasks("milk")
    assert len(results) == 1
    assert results[0].title == "Buy milk"

    # Search by description
    results = task_service.search_tasks("park")
    assert len(results) == 1
    assert results[0].title == "Walk the dog"

    # Search by keyword present in both
    task_service.add_task("Milk and bread", description="Get milk and bread.")
    results = task_service.search_tasks("milk")
    assert len(results) == 2
    
def test_filter_tasks(task_service: TaskService):
    from datetime import date, timedelta
    today = date.today()
    task1 = task_service.add_task("Task 1", priority="High", tags=["work", "urgent"], due_date=today + timedelta(days=1), description="Description 1")
    task_service.update_task(task1.id, is_completed=True)
    task2 = task_service.add_task("Task 2", priority="Medium", tags=["home"], due_date=today + timedelta(days=2), description="Description 2")
    task_service.update_task(task2.id, is_completed=False)
    # Task 3: completed=True, priority=Low, tags=["personal", "urgent"], due_date=today + timedelta(days=5), description="Description 3")
    task3 = task_service.add_task("Task 3", priority="Low", tags=["personal", "urgent"], due_date=today + timedelta(days=5), description="Description 3")
    task_service.update_task(task3.id, is_completed=True)
    
    # Task 4: completed=False, priority=High, tags=["work"], due_date=today + 2 days
    task4 = task_service.add_task("Task 4", priority="High", tags=["work"], due_date=today + timedelta(days=2), description="Description 4")
    task_service.update_task(task4.id, is_completed=False)

    # Filter by completed
    completed_tasks = task_service.filter_tasks(completed=True)
    assert len(completed_tasks) == 2
    assert task1 in completed_tasks
    assert task3 in completed_tasks

    # Filter by priority
    high_priority_tasks = task_service.filter_tasks(priority="High")
    assert len(high_priority_tasks) == 2
    assert task1 in high_priority_tasks
    assert task4 in high_priority_tasks

    # Filter by tags
    work_tasks = task_service.filter_tasks(tags=["work"])
    assert len(work_tasks) == 2
    assert task1 in work_tasks
    assert task4 in work_tasks
    
    urgent_tasks = task_service.filter_tasks(tags=["urgent"])
    assert len(urgent_tasks) == 2
    assert task1 in urgent_tasks
    assert task3 in urgent_tasks

    # Filter by due_before
    # task1 is due today + 1 day.
    # So, filtering "due_before = today + 1 day" should include only tasks due on or before today + 1 day.
    # This includes task1. No other tasks should be included.
    due_before_tasks = task_service.filter_tasks(due_before=today + timedelta(days=1))
    assert len(due_before_tasks) == 1
    assert task1 in due_before_tasks
    assert task2 not in due_before_tasks # task2 is due today + 2 days

    # Filter by due_after
    # All tasks (task1, task2, task3, task4) are due on or after `today + 1 day`
    due_after_tasks = task_service.filter_tasks(due_after=today + timedelta(days=1))
    assert len(due_after_tasks) == 4
    assert task1 in due_after_tasks
    assert task2 in due_after_tasks
    assert task3 in due_after_tasks
    assert task4 in due_after_tasks

    # Combine filters: completed=True, priority="Low", tags=["urgent"]
    combined_filters = task_service.filter_tasks(completed=True, priority="Low", tags=["urgent"])
    assert len(combined_filters) == 1
    assert task3 in combined_filters
    
    # Combine filters: completed=False, priority="High", tags=["work"], due_after=today + timedelta(days=1)
    combined_filters_2 = task_service.filter_tasks(completed=False, priority="High", tags=["work"], due_after=today + timedelta(days=1))
    assert len(combined_filters_2) == 1
    assert task4 in combined_filters_2


def test_sort_tasks(task_service: TaskService):
    from datetime import date, timedelta
    today = date.today()
    task1 = task_service.add_task("Task B", due_date=today + timedelta(days=2), priority="Medium")
    task2 = task_service.add_task("Task A", due_date=today + timedelta(days=1), priority="High")
    task3 = task_service.add_task("Task C", due_date=today + timedelta(days=3), priority="Low")

    # Sort by due_date
    sorted_by_date = task_service.sort_tasks(sort_by="due_date")
    assert sorted_by_date[0].id == task2.id
    assert sorted_by_date[1].id == task1.id
    assert sorted_by_date[2].id == task3.id

    # Sort by priority
    sorted_by_priority = task_service.sort_tasks(sort_by="priority")
    assert sorted_by_priority[0].id == task2.id # High
    assert sorted_by_priority[1].id == task1.id # Medium
    assert sorted_by_priority[2].id == task3.id # Low

    # Sort by title
    sorted_by_title = task_service.sort_tasks(sort_by="title")
    assert sorted_by_title[0].id == task2.id # Task A
    assert sorted_by_title[1].id == task1.id # Task B
    assert sorted_by_title[2].id == task3.id # Task C

def test_add_task_with_invalid_priority():
    from src.models.task import Task
    with pytest.raises(ValueError, match="Invalid priority"):
        Task("Invalid Priority Task", priority="Urgent")

from unittest.mock import patch
from io import StringIO
from src.cli.main import main

@patch('builtins.input', side_effect=['1', 'CLI Test Task', '', 'High', 'work personal', '2025-12-25', '', '', '', '2', 'n', 'None', '0'])
@patch('sys.stdout', new_callable=StringIO)
def test_cli_add_and_list_task_with_priority_and_tags(mock_stdout, mock_input):
    main()
    output = mock_stdout.getvalue()
    assert "Added task: 'CLI Test Task'" in output
    assert "CLI Test Task" in output
    assert "🔴" in output  # High priority emoji
    assert "(work, personal)" in output
    assert "Due: 2025-12-25" in output

@patch('builtins.input', side_effect=[
    '1', # Menu choice: Add Task
    'Task for Search One', # Title
    '', # Description (default)
    'Medium', # Priority
    'tag1', # Tags
    '2025-12-25', # Due Date
    '', # Due Time (default)
    '', # Recurrence Type (default)
    '', # Reminder Minutes (default)
    
    '1', # Menu choice: Add Task
    'Task for Search Two', # Title
    '', # Description (default)
    'Low', # Priority
    'tag2', # Tags
    '2025-12-26', # Due Date
    '', # Due Time (default)
    '', # Recurrence Type (default)
    '', # Reminder Minutes (default)
    
    '8', 'Search One', # Menu choice: Search Tasks, Keyword
    '0' # Menu choice: Exit
])
@patch('sys.stdout', new_callable=StringIO)
def test_cli_search_tasks(mock_stdout, mock_input):
    main()
    output = mock_stdout.getvalue()
    # Assert tasks were added
    assert "Added task: 'Task for Search One'" in output
    assert "Added task: 'Task for Search Two'" in output
    # Assert search results are correct
    search_results_start = output.find("--- Search Results for 'Search One' ---")
    search_results_end = output.find("---------------------------------------", search_results_start)
    search_results_output = output[search_results_start:search_results_end]

    assert "Task for Search One" in search_results_output
    assert "Task for Search Two" not in search_results_output # Task Two should not be in search results

# @patch('builtins.input', side_effect=[
#     '1', # Menu choice: Add Task
#     'Filtered Task High', # Title
#     '', # Description (default)
#     'High', # Priority
#     'tag1', # Tags
#     '2025-12-30', # Due Date
#     '', # Due Time (default)
#     '', # Recurrence Type (default)
#     '', # Reminder Minutes (default)
    
#     '1', # Menu choice: Add Task
#     'Filtered Task Low', # Title
#     '', # Description (default)
#     'Low', # Priority
#     'tag2', # Tags
#     '2025-12-20', # Due Date
#     '', # Due Time (default)
#     '', # Recurrence Type (default)
#     '', # Reminder Minutes (default)
    
#     '2', # Menu choice: List All Tasks
#     'y', # Apply filters?
#     'y', # Filter by completed status (y)
#     'High', # Filter by priority (High)
#     '', # Filter by tags (empty)
#     '', # Filter due before date (empty)
#     '', # Filter due after date (empty)
#     'None', # Sorting choice (new prompt)
#     '0' # Menu choice: Exit
# ])
# @patch('sys.stdout', new_callable=StringIO)
# def test_cli_filter_tasks(mock_stdout, mock_input):
#     try:
#         main()
#     except StopIteration:
#         pytest.fail("StopIteration occurred. Not enough side_effect inputs for 'input()'.")
#     except Exception as e:
#         pytest.fail(f"An unexpected exception occurred: {e}")

#     output = mock_stdout.getvalue()
#     # Assert tasks were added
#     assert "Added task: 'Filtered Task High'" in output
#     assert "Added task: 'Filtered Task Low'" in output
#     # Assert filtered results are correct
#     filtered_results_start = output.find("--- Your Filtered Tasks ---")
#     filtered_results_end = output.find("---------------------------", filtered_results_start)
#     filtered_results_output = output[filtered_results_start:filtered_results_end]

#     assert "Filtered Task High" in filtered_results_output
#     assert "Filtered Task Low" not in filtered_results_output
#     assert "🔴" in filtered_results_output # High priority emoji



