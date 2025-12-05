import uuid
from datetime import date, time, datetime, timezone
from typing import List, Optional, Dict, Any

class Task:
    """
    Represents a single to-do item with various attributes.
    """
    def __init__(self, title: str,
                 id: Optional[str] = None,
                 is_completed: bool = False, # Renamed from 'completed'
                 priority: str = "Medium",
                 tags: Optional[List[str]] = None,
                 due_date: Optional[date] = None, # Changed type from datetime to date
                 due_time: Optional[time] = None, # New attribute
                 recurrence_type: Optional[str] = None, # Replaces is_recurring and recurrence_rule
                 reminder_minutes_before_due: Optional[int] = None, # New attribute
                 original_recurring_task_id: Optional[str] = None, # New attribute
                 description: Optional[str] = None):
        """
        Initializes a new Task object.

        Args:
            title (str): The description of the task.
            id (Optional[str]): The unique identifier for the task. If None, a new UUID will be generated.
            is_completed (bool): The completion status of the task. Defaults to False.
            priority (str): The priority of the task (e.g., "High", "Medium", "Low"). Defaults to "Medium".
            tags (Optional[List[str]]): A list of tags associated with the task. Defaults to an empty list.
            due_date (Optional[date]): The due date for the task. Defaults to None.
            due_time (Optional[time]): The due time for the task. Defaults to None.
            recurrence_type (Optional[str]): Type of recurrence (e.g., "Daily", "Weekly", "Monthly"). Defaults to None.
            reminder_minutes_before_due (Optional[int]): Minutes before due_date/time to trigger a reminder. Defaults to None.
            original_recurring_task_id (Optional[str]): ID of the parent recurring task if this is an instance. Defaults to None.
            description (Optional[str]): A longer description for the task. Defaults to None.
        """
        self.id: str = id if id else str(uuid.uuid4())
        self.title: str = title
        self.is_completed: bool = is_completed # Renamed
        if priority not in ["High", "Medium", "Low"]:
            raise ValueError(f"Invalid priority: {priority}. Must be 'High', 'Medium', or 'Low'.")
        self.priority: str = priority
        self.tags: List[str] = tags if tags is not None else []
        self.due_date: Optional[date] = due_date # Changed type
        self.due_time: Optional[time] = due_time # New
        self.recurrence_type: Optional[str] = recurrence_type # Replaces is_recurring and recurrence_rule
        self.reminder_minutes_before_due: Optional[int] = reminder_minutes_before_due # New
        self.original_recurring_task_id: Optional[str] = original_recurring_task_id # New
        self.description: Optional[str] = description
        




    def is_overdue(self, current_datetime: Optional[datetime] = None) -> bool: # Changed to method with argument
        """
        Checks if the task is overdue.

        Args:
            current_datetime (Optional[datetime]): The datetime to use as "now" for checking overdue status.
                                                  Defaults to datetime.now(timezone.utc) if None.

        Returns:
            bool: True if the task is overdue, False otherwise.
        """
        if self.is_completed or not self.due_date:
            return False

        now_to_use = current_datetime if current_datetime else datetime.now(timezone.utc)
        due_datetime = datetime.combine(self.due_date, self.due_time if self.due_time else time(23, 59, 59), tzinfo=timezone.utc)

        return due_datetime < now_to_use

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Task object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the task.
        """
        return {
            "id": self.id,
            "title": self.title,
            "is_completed": self.is_completed, # Renamed
            "priority": self.priority,
            "tags": self.tags,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "due_time": self.due_time.isoformat() if self.due_time else None, # New
            "recurrence_type": self.recurrence_type, # Replaces is_recurring and recurrence_rule
            "reminder_minutes_before_due": self.reminder_minutes_before_due, # New
            "original_recurring_task_id": self.original_recurring_task_id, # New
            "description": self.description
        }




    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Task':
        """
        Creates a Task object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing task data.

        Returns:
            Task: A new Task object.
        """
        return Task(
            id=data["id"],
            title=data["title"],
            is_completed=data["is_completed"], # Renamed
            priority=data["priority"],
            tags=data["tags"],
            due_date=date.fromisoformat(data["due_date"]) if data["due_date"] else None, # Changed deserialization
            due_time=time.fromisoformat(data["due_time"]) if data["due_time"] else None, # New deserialization
            recurrence_type=data.get("recurrence_type"), # Replaces is_recurring and recurrence_rule
            reminder_minutes_before_due=data.get("reminder_minutes_before_due"), # New
            original_recurring_task_id=data.get("original_recurring_task_id"), # New
            description=data["description"]
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the Task object.

        Returns:
            str: A string representation suitable for debugging.
        """
        return (f"Task(id='{self.id}', title='{self.title}', is_completed={self.is_completed}, "
                f"priority='{self.priority}', tags={self.tags}, due_date={self.due_date}, "
                f"due_time={self.due_time}, recurrence_type='{self.recurrence_type}', "
                f"reminder_minutes_before_due={self.reminder_minutes_before_due}, "
                f"original_recurring_task_id='{self.original_recurring_task_id}', "
                f"description='{self.description}')")
