from typing import Dict, List, Optional
from src.models.notification import Notification
from datetime import datetime, timezone, timedelta
from src.models.task import Task # New import

class NotificationService:
    """
    Manages a collection of notifications in-memory, providing CRUD and retrieval functionalities.
    """
    def __init__(self):
        """
        Initializes the NotificationService with an empty dictionary to store notifications.
        """
        self._notifications: Dict[str, Notification] = {}

    def schedule_reminder(self, task: Task) -> Optional[Notification]:
        """
        Schedules a reminder notification for a given task.

        Args:
            task (Task): The task for which to schedule a reminder.

        Returns:
            Optional[Notification]: The created Notification object if scheduled, None otherwise.
        """
        if not task.due_date or not task.due_time or task.reminder_minutes_before_due is None or task.is_completed:
            return None

        # Combine date and time, make it timezone aware (UTC)
        due_datetime = datetime.combine(task.due_date, task.due_time, tzinfo=timezone.utc)
        
        trigger_time = due_datetime - timedelta(minutes=task.reminder_minutes_before_due)

        # Ensure trigger time is in the future relative to now, otherwise it's already past
        if trigger_time <= datetime.now(timezone.utc):
            return None # Don't schedule reminders for past events

        message = f"Reminder: '{task.title}' is due at {task.due_time.strftime('%H:%M')} on {task.due_date.strftime('%Y-%m-%d')}!"
        
        # Check if a similar notification already exists to avoid duplicates
        # A more robust check might involve comparing trigger_time and message as well
        existing_notifications = [n for n in self._notifications.values() 
                                  if n.task_id == task.id and n.trigger_time == trigger_time and not n.is_delivered]
        if existing_notifications:
            return existing_notifications[0] # Return existing pending notification

        notification = self.add_notification(message, task.id, trigger_time)
        return notification

    def add_notification(self, message: str, task_id: str, trigger_time: datetime) -> Notification:
        """
        Adds a new notification to the service.

        Args:
            message (str): The content of the notification.
            task_id (str): The ID of the task this notification is for.
            trigger_time (datetime): The exact UTC time the notification should be displayed/pushed.

        Returns:
            Notification: The newly created Notification object.
        """
        notification = Notification(message=message, task_id=task_id, trigger_time=trigger_time)
        self._notifications[notification.id] = notification
        return notification

    def get_notification(self, notification_id: str) -> Optional[Notification]:
        """
        Retrieves a notification by its ID.

        Args:
            notification_id (str): The unique ID of the notification.

        Returns:
            Optional[Notification]: The Notification object if found, otherwise None.
        """
        return self._notifications.get(notification_id)

    def get_all_notifications(self) -> List[Notification]:
        """
        Retrieves all notifications currently in the service.

        Returns:
            List[Notification]: A list of all Notification objects.
        """
        return list(self._notifications.values())

    def get_pending_notifications(self, current_time: datetime) -> List[Notification]:
        """
        Retrieves all notifications that are due to be triggered at or before the current_time
        and have not yet been delivered.

        Args:
            current_time (datetime): The current UTC time to check against.

        Returns:
            List[Notification]: A list of pending Notification objects.
        """
        pending = [
            n for n in self._notifications.values()
            if n.trigger_time <= current_time and not n.is_delivered
        ]
        return pending

    def mark_notification_delivered(self, notification_id: str) -> Optional[Notification]:
        """
        Marks a notification as delivered.

        Args:
            notification_id (str): The ID of the notification to mark as delivered.

        Returns:
            Optional[Notification]: The updated Notification object if found, otherwise None.
        """
        notification = self._notifications.get(notification_id)
        if notification:
            notification.is_delivered = True
            notification.delivered_at = datetime.now(timezone.utc) # Use UTC for consistency
            return notification
        return None
    
    def delete_notification(self, notification_id: str) -> bool:
        """
        Deletes a notification by its ID.

        Args:
            notification_id (str): The ID of the notification to delete.

        Returns:
            bool: True if the notification was deleted, False otherwise.
        """
        if notification_id in self._notifications:
            del self._notifications[notification_id]
            return True
        return False