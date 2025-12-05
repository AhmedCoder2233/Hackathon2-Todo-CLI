from typing import List, Dict, Optional
from datetime import datetime, date, time, timezone
from src.models.task import Task
from src.lib.recurrence_util import get_next_recurrence_date

class TaskService:
    """
    Manages a collection of tasks in-memory, providing CRUD, search, filter, and sort functionalities.
    """
    def __init__(self):
        """
        Initializes the TaskService with an empty dictionary to store tasks.
        """
        self._tasks: Dict[str, Task] = {}

    def _generate_next_recurring_instance(self, original_task: Task) -> Task:
        """
        Helper method to generate the next instance of a recurring task.
        (Implementation details will be in T019)
        """
        if original_task.recurrence_type is None:
            raise ValueError("Task is not recurring.")

        next_due_date = get_next_recurrence_date(original_task.due_date, original_task.recurrence_type)

        new_task = Task(
            title=original_task.title,
            description=original_task.description,
            priority=original_task.priority,
            tags=original_task.tags,
            due_date=next_due_date,
            due_time=original_task.due_time,
            recurrence_type=original_task.recurrence_type,
            reminder_minutes_before_due=original_task.reminder_minutes_before_due,
            original_recurring_task_id=original_task.id
        )
        self.add_task(
            title=new_task.title,
            description=new_task.description,
            priority=new_task.priority,
            tags=new_task.tags,
            due_date=new_task.due_date,
            due_time=new_task.due_time,
            recurrence_type=new_task.recurrence_type,
            reminder_minutes_before_due=new_task.reminder_minutes_before_due,
            original_recurring_task_id=new_task.original_recurring_task_id
        )
        return new_task

    def add_task(self, title: str,
                 is_completed: bool = False,
                 priority: str = "Medium",
                 tags: Optional[List[str]] = None,
                 due_date: Optional[date] = None,
                 due_time: Optional[time] = None,
                 recurrence_type: Optional[str] = None,
                 reminder_minutes_before_due: Optional[int] = None,
                 original_recurring_task_id: Optional[str] = None,
                 description: Optional[str] = None) -> Task:
        """
        Adds a new task to the service.
        """
        if due_date and due_date < datetime.now(timezone.utc).date():
            raise ValueError("Due date cannot be in the past.")
        if due_time is not None and not isinstance(due_time, time):
            raise ValueError("Due time must be a valid time object (HH:MM).")
        
        task = Task(title=title, is_completed=is_completed, priority=priority, tags=tags,
                    due_date=due_date, due_time=due_time, recurrence_type=recurrence_type,
                    reminder_minutes_before_due=reminder_minutes_before_due,
                    original_recurring_task_id=original_recurring_task_id,
                    description=description)
        self._tasks[task.id] = task
        return task

    def create_recurring_task(self, title: str,
                              recurrence_type: str,
                              priority: str = "Medium",
                              tags: Optional[List[str]] = None,
                              due_date: Optional[date] = None,
                              due_time: Optional[time] = None,
                              reminder_minutes_before_due: Optional[int] = None,
                              description: Optional[str] = None) -> Task:
        """
        Creates a new recurring task. This is a specialized version of add_task.
        """
        if recurrence_type not in ["Daily", "Weekly", "Monthly"]:
            raise ValueError("Invalid recurrence type. Must be 'Daily', 'Weekly', or 'Monthly'.")

        existing_duplicates = [
            task for task in self._tasks.values()
            if task.title == title and
               task.due_date == due_date and
               task.recurrence_type == recurrence_type and
               not task.is_completed
        ]
        if existing_duplicates:
            raise ValueError("A recurring task with the same title, due date, and recurrence type already exists and is not completed.")

        return self.add_task(
            title=title,
            priority=priority,
            tags=tags,
            due_date=due_date,
            due_time=due_time,
            recurrence_type=recurrence_type,
            reminder_minutes_before_due=reminder_minutes_before_due,
            description=description
        )

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Retrieves a task by its ID.
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieves all tasks currently in the service.
        """
        return list(self._tasks.values())

    def update_task(self, task_id: str,
                    title: Optional[str] = None,
                    is_completed: Optional[bool] = None,
                    priority: Optional[str] = None,
                    tags: Optional[List[str]] = None,
                    due_date: Optional[date] = None,
                    due_time: Optional[time] = None,
                    recurrence_type: Optional[str] = None,
                    reminder_minutes_before_due: Optional[int] = None,
                    original_recurring_task_id: Optional[str] = None,
                    description: Optional[str] = None) -> Optional[Task]:
        """
        Updates an existing task's attributes.
        """
        task = self._tasks.get(task_id)
        if task:
            original_is_completed_state = task.is_completed

            if title is not None:
                task.title = title
            if is_completed is not None:
                task.is_completed = is_completed
                if task.is_completed and not original_is_completed_state and task.recurrence_type:
                    self._generate_next_recurring_instance(task)
            if priority is not None:
                task.priority = priority
            if tags is not None:
                task.tags = tags
            if due_date is not None:
                if due_date < datetime.now(timezone.utc).date():
                    raise ValueError("Due date cannot be in the past.")
                task.due_date = due_date
            if due_time is not None:
                if not isinstance(due_time, time):
                    raise ValueError("Due time must be a valid time object (HH:MM).")
                task.due_time = due_time
            if recurrence_type is not None:
                task.recurrence_type = recurrence_type
            if reminder_minutes_before_due is not None:
                task.reminder_minutes_before_due = reminder_minutes_before_due
            if original_recurring_task_id is not None:
                task.original_recurring_task_id = original_recurring_task_id
            if description is not None:
                task.description = description
            return task
        return None

    def delete_task(self, task_id: str) -> bool:
        """
        Deletes a task by its ID.
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Searches tasks by a keyword present in their title.
        """
        return [task for task in self._tasks.values() 
                if keyword.lower() in task.title.lower() or 
                (task.description and keyword.lower() in task.description.lower())]

    def filter_tasks(self, completed: Optional[bool] = None, 
                     priority: Optional[str] = None, 
                     tags: Optional[List[str]] = None,
                     due_before: Optional[date] = None,
                     due_after: Optional[date] = None) -> List[Task]:
        """
        Filters tasks based on their completion status, priority, tags, and due date range.
        """
        filtered_tasks = list(self._tasks.values())
        if completed is not None:
            filtered_tasks = [task for task in filtered_tasks if task.is_completed == completed]
        if priority is not None:
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority]
        if tags is not None:
            filtered_tasks = [task for task in filtered_tasks if any(tag in task.tags for tag in tags)]
        if due_before is not None:
            filtered_tasks = [task for task in filtered_tasks if task.due_date and task.due_date <= due_before]
        if due_after is not None:
            filtered_tasks = [task for task in filtered_tasks if task.due_date and task.due_date >= due_after]
        return filtered_tasks

    def sort_tasks(self, sort_by: str = "title") -> List[Task]:
        """
        Sorts tasks based on a specified attribute.
        """
        priority_map = {"High": 3, "Medium": 2, "Low": 1}

        if sort_by == "due_date":
            return sorted(self._tasks.values(), key=lambda task: (task.due_date is None, task.due_date))
        elif sort_by == "priority":
            return sorted(self._tasks.values(), key=lambda task: priority_map.get(task.priority, 0), reverse=True)
        elif sort_by == "title":
            return sorted(self._tasks.values(), key=lambda task: task.title.lower())
        else:
            return list(self._tasks.values())

    def get_overdue_tasks(self, current_datetime: Optional[datetime] = None) -> List[Task]:
        """
        Retrieves all tasks that are currently overdue and not completed.
        """
        return [task for task in self._tasks.values() if task.is_overdue(current_datetime)]