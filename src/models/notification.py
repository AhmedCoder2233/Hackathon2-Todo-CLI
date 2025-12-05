import uuid
from datetime import datetime
from typing import Dict, Any, Optional

class Notification:
    """
    Represents a scheduled or triggered alert for a task reminder.
    """
    def __init__(self, message: str,
                 task_id: str,
                 trigger_time: datetime,
                 id: Optional[str] = None,
                 is_delivered: bool = False,
                 delivered_at: Optional[datetime] = None):
        """
        Initializes a new Notification object.

        Args:
            message (str): The content of the notification.
            task_id (str): The ID of the Task this notification is for.
            trigger_time (datetime): The exact UTC time the notification should be displayed/pushed.
            id (Optional[str]): The unique identifier for the notification. If None, a new UUID will be generated.
            is_delivered (bool): Indicates if the notification has been successfully delivered/displayed.
            delivered_at (Optional[datetime]): Timestamp of when the notification was delivered.
        """
        self.id: str = id if id else str(uuid.uuid4())
        self.message: str = message
        self.task_id: str = task_id
        self.trigger_time: datetime = trigger_time
        self.is_delivered: bool = is_delivered
        self.delivered_at: Optional[datetime] = delivered_at

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Notification object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the notification.
        """
        return {
            "id": self.id,
            "message": self.message,
            "task_id": self.task_id,
            "trigger_time": self.trigger_time.isoformat(),
            "is_delivered": self.is_delivered,
            "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Notification':
        """
        Creates a Notification object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing notification data.

        Returns:
            Notification: A new Notification object.
        """
        return Notification(
            id=data["id"],
            message=data["message"],
            task_id=data["task_id"],
            trigger_time=datetime.fromisoformat(data["trigger_time"]),
            is_delivered=data["is_delivered"],
            delivered_at=datetime.fromisoformat(data["delivered_at"]) if data["delivered_at"] else None
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the Notification object.

        Returns:
            str: A string representation suitable for debugging.
        """
        return (f"Notification(id='{self.id}', task_id='{self.task_id}', "
                f"trigger_time={self.trigger_time}, is_delivered={self.is_delivered})")
