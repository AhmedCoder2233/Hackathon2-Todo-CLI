from datetime import datetime, timedelta, timezone
import pytest
from src.models.notification import Notification
from src.services.notification_service import NotificationService

def test_add_notification():
    """
    Tests that a notification can be successfully added to the service.
    """
    service = NotificationService()
    message = "Task Due Soon"
    task_id = "task-123"
    trigger_time = datetime.now(timezone.utc) + timedelta(minutes=10)

    notification = service.add_notification(message, task_id, trigger_time)

    assert notification is not None
    assert notification.message == message
    assert notification.task_id == task_id
    assert notification.trigger_time == trigger_time
    assert notification.id in service._notifications
    assert service.get_notification(notification.id) == notification

def test_get_notification():
    """
    Tests that a notification can be retrieved by its ID.
    """
    service = NotificationService()
    message = "Test Notification"
    task_id = "task-456"
    trigger_time = datetime.now(timezone.utc) + timedelta(minutes=5)
    added_notification = service.add_notification(message, task_id, trigger_time)

    retrieved_notification = service.get_notification(added_notification.id)
    assert retrieved_notification == added_notification

    # Test for non-existent notification
    non_existent_notification = service.get_notification("non-existent-id")
    assert non_existent_notification is None

def test_get_all_notifications():
    """
    Tests that all notifications can be retrieved from the service.
    """
    service = NotificationService()
    notification1 = service.add_notification("Msg1", "task1", datetime.now(timezone.utc) + timedelta(minutes=1))
    notification2 = service.add_notification("Msg2", "task2", datetime.now(timezone.utc) + timedelta(minutes=2))

    all_notifications = service.get_all_notifications()
    assert len(all_notifications) == 2
    assert notification1 in all_notifications
    assert notification2 in all_notifications

def test_get_pending_notifications():
    """
    Tests retrieval of pending notifications based on current time and delivery status.
    """
    service = NotificationService()
    now = datetime.now(timezone.utc)

    # Pending notification (due in past, not delivered)
    pending_notif = service.add_notification("Pending", "t1", now - timedelta(minutes=5))
    # Future notification (not yet due)
    service.add_notification("Future", "t2", now + timedelta(minutes=5))
    # Delivered notification (due in past, delivered)
    delivered_notif = service.add_notification("Delivered", "t3", now - timedelta(minutes=10))
    service.mark_notification_delivered(delivered_notif.id)

    pending = service.get_pending_notifications(now)
    assert len(pending) == 1
    assert pending[0].id == pending_notif.id

def test_mark_notification_delivered():
    """
    Tests marking a notification as delivered.
    """
    service = NotificationService()
    notification = service.add_notification("Deliver Me", "task-del", datetime.now(timezone.utc) - timedelta(minutes=1))

    assert notification.is_delivered is False
    assert notification.delivered_at is None

    delivered_notif = service.mark_notification_delivered(notification.id)
    assert delivered_notif is not None
    assert delivered_notif.is_delivered is True
    assert delivered_notif.delivered_at is not None
    assert service.get_notification(notification.id).is_delivered is True

    # Test marking non-existent notification
    assert service.mark_notification_delivered("non-existent") is None

def test_delete_notification():
    """
    Tests deleting a notification.
    """
    service = NotificationService()
    notification = service.add_notification("Delete Me", "task-del", datetime.now(timezone.utc) + timedelta(minutes=1))

    assert service.get_notification(notification.id) is not None
    
    deleted = service.delete_notification(notification.id)
    assert deleted is True
    assert service.get_notification(notification.id) is None

    # Test deleting non-existent notification
    assert service.delete_notification("non-existent") is False