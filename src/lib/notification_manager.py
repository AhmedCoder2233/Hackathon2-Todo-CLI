from datetime import datetime, timezone
from src.services.notification_service import NotificationService
from src.models.notification import Notification
from typing import List, Callable, Optional

class NotificationManager:
    """
    Manages the periodic checking and triggering of notifications.
    """
    def __init__(self, notification_service: NotificationService, trigger_callback: Optional[Callable[[Notification], None]] = None):
        """
        Initializes the NotificationManager.

        Args:
            notification_service (NotificationService): An instance of NotificationService.
            trigger_callback (Optional[Callable[[Notification], None]]): A callback function
                                                                        to execute when a notification is triggered.
                                                                        If None, a default print action is used.
        """
        self.notification_service = notification_service
        self.trigger_callback = trigger_callback if trigger_callback else self._default_trigger_callback

    def _default_trigger_callback(self, notification: Notification):
        """
        Default callback for triggering a notification (prints to console).
        """
        print(f"\n🔔 Notification: {notification.message} (Task ID: {notification.task_id})")

    def process_pending_notifications(self) -> List[Notification]:
        """
        Checks for and processes all pending notifications.

        Returns:
            List[Notification]: A list of notifications that were triggered.
        """
        current_time = datetime.now(timezone.utc)
        pending_notifications = self.notification_service.get_pending_notifications(current_time)
        
        triggered_notifications: List[Notification] = []
        for notification in pending_notifications:
            self.trigger_callback(notification)
            self.notification_service.mark_notification_delivered(notification.id)
            triggered_notifications.append(notification)
            
        return triggered_notifications

    # In a real application, this would be run periodically by a scheduler
    # For a CLI, it might be triggered by a specific command or on startup

