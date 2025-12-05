import argparse
import sys
import os
from datetime import datetime, date, time, timezone
from typing import List, Optional, Dict, Any
from zoneinfo import ZoneInfo

# Define Karachi Timezone
KARACHI_TIMEZONE = ZoneInfo("Asia/Karachi")

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.services.task_service import TaskService
from src.services.notification_service import NotificationService
from src.lib.notification_manager import NotificationManager
from src.models.task import Task

def print_menu():
    """Prints the main menu for the to-do application."""
    print("\n--- To-Do List Menu ---")
    print("1. Add Task")
    print("2. List All Tasks")
    print("3. Update Task")
    print("4. Mark Task as Complete")
    print("5. Delete Task")
    print("6. Set Task Priority")
    print("7. Add Tags to Task")
    print("8. Search Tasks")
    print("9. Process Notifications")
    print("10. Sort Tasks")
    print("0. Exit")
    print("-----------------------")

def get_task_details_from_input(task: Optional[Task] = None) -> Dict[str, Any]:
    """
    Helper function to get new or updated task details from user input.
    """
    details = {}

    title = input(f"Enter title [{task.title if task else 'None'}]: ")
    if title:
        details["title"] = title

    description = input(f"Enter description [{task.description if task else 'None'}]: ")
    if description:
        details["description"] = description

    priority = input(f"Enter priority (High, Medium, Low) [{task.priority if task else 'Medium'}]: ")
    if priority and priority in ["High", "Medium", "Low"]:
        details["priority"] = priority

    tags_input = input(f"Enter tags (space-separated) [{', '.join(task.tags) if task and task.tags else 'None'}]: ")
    if tags_input:
        details["tags"] = tags_input.split()

    # For displaying existing date/time in Karachi time
    karachi_due_date_display = None
    karachi_due_time_display = None
    if task and task.due_date and task.due_time:
        # Assume stored date and time are UTC, combine them
        utc_datetime = datetime.combine(task.due_date, task.due_time, tzinfo=timezone.utc)
        # Convert to Karachi timezone for display
        karachi_datetime = utc_datetime.astimezone(KARACHI_TIMEZONE)
        karachi_due_date_display = karachi_datetime.date()
        karachi_due_time_display = karachi_datetime.time()
    elif task and task.due_date:
        # If only date is set, assume 00:00:00 UTC and convert to Karachi
        utc_datetime = datetime.combine(task.due_date, time(0,0,0), tzinfo=timezone.utc)
        karachi_datetime = utc_datetime.astimezone(KARACHI_TIMEZONE)
        karachi_due_date_display = karachi_datetime.date()
    
    due_date_str = input(f"Enter due date (YYYY-MM-DD) [{karachi_due_date_display.strftime('%Y-%m-%d') if karachi_due_date_display else 'None'}]: ")
    parsed_date = None
    if due_date_str:
        try:
            parts = [int(p) for p in due_date_str.split('-')]
            if len(parts) == 3:
                parsed_date = date(parts[0], parts[1], parts[2])
            else:
                raise ValueError("Incorrect number of date parts.")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD. Due date not set.")
            parsed_date = None
    elif task and karachi_due_date_display and not due_date_str:
        details["due_date"] = None
    
    due_time_str = input(f"Enter due time (HH:MM AM/PM) [{karachi_due_time_display.strftime('%I:%M %p') if karachi_due_time_display else 'None'}]: ")
    parsed_time = None
    if due_time_str:
        try:
            parsed_time = datetime.strptime(due_time_str, '%I:%M %p').time()
        except ValueError:
            print("Invalid time format. Please use HH:MM AM/PM. Due time not set.")
            parsed_time = None
    elif task and karachi_due_time_display and not due_time_str:
        details["due_time"] = None

    # Perform Karachi to UTC conversion if both date and time were provided/parsed successfully
    if parsed_date and parsed_time:
        try:
            # Combine naive date and time, then make it timezone-aware in Karachi, then convert to UTC
            naive_datetime = datetime.combine(parsed_date, parsed_time)
            karachi_aware_datetime = naive_datetime.replace(tzinfo=KARACHI_TIMEZONE)
            utc_datetime = karachi_aware_datetime.astimezone(timezone.utc)
            
            details["due_date"] = utc_datetime.date()
            details["due_time"] = utc_datetime.time()
        except Exception as e:
            print(f"Error converting to Karachi time and UTC: {e}. Due date/time not set.")
    elif parsed_date and (details.get("due_time") is None):
        # If only date is provided/updated, store it. The time will be None internally.
        # When Task combines, it uses 00:00:00 for time. This implicitly means 00:00:00 UTC.
        details["due_date"] = parsed_date

    recurrence_type = input(f"Enter recurrence type (Daily, Weekly, Monthly) [{task.recurrence_type if task else 'None'}]: ")
    if recurrence_type and recurrence_type in ["Daily", "Weekly", "Monthly", "None"]:
        details["recurrence_type"] = recurrence_type if recurrence_type != "None" else None
    elif task and task.recurrence_type and not recurrence_type:
        details["recurrence_type"] = None

    reminder_minutes_str = input(f"Enter reminder minutes before due [{task.reminder_minutes_before_due if task else 'None'}]: ")
    if reminder_minutes_str:
        try:
            details["reminder_minutes_before_due"] = int(reminder_minutes_str)
        except ValueError:
            print("Invalid number for reminder minutes. Reminder not set.")
    elif task and task.reminder_minutes_before_due and not reminder_minutes_str:
        details["reminder_minutes_before_due"] = None
            
    return details


def main():
    """
    Main function for the interactive to-do application.

    Runs a continuous loop that displays a menu of options and performs
    actions on tasks based on user input.
    """
    task_service = TaskService()
    notification_service = NotificationService()
    notification_manager = NotificationManager(notification_service)

    print("Welcome to your To-Do List!")

    while True:
        notification_manager.process_pending_notifications()
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n--- Add New Task ---")
            details = get_task_details_from_input()
            
            # Ensure title is provided for new tasks
            if "title" not in details or not details["title"]:
                print("❌ Task title is required.")
                continue

            try:
                task = task_service.add_task(**details)
                print(f"\n✅ Added task: '{task.title}' (ID: {task.id})")
                notification_service.schedule_reminder(task)
            except ValueError as e:
                print(f"\n❌ Error adding task: {e}")

        elif choice == "2":
            print("\n--- List Tasks ---")
            filter_choice = input("Apply filters? (y/n) [n]: ").lower()
            
            filter_completed: Optional[bool] = None
            filter_priority: Optional[str] = None
            filter_tags: Optional[List[str]] = None
            filter_due_before: Optional[date] = None
            filter_due_after: Optional[date] = None

            if filter_choice == 'y':
                completed_input = input("Filter by completed status (y/n/all) [all]: ").lower()
                if completed_input == 'y':
                    filter_completed = True
                elif completed_input == 'n':
                    filter_completed = False

                priority_input = input("Filter by priority (High, Medium, Low, all) [all]: ")
                if priority_input in ["High", "Medium", "Low"]:
                    filter_priority = priority_input

                tags_input = input("Filter by tags (space-separated, leave blank for all) [all]: ")
                if tags_input:
                    filter_tags = tags_input.split()
                
                due_before_str = input("Filter due before date (YYYY-MM-DD, leave blank for all) [all]: ")
                if due_before_str:
                    try:
                        filter_due_before = date.fromisoformat(due_before_str)
                    except ValueError:
                        print("Invalid date format. Ignoring due date before filter.")
                
                due_after_str = input("Filter due after date (YYYY-MM-DD, leave blank for all) [all]: ")
                if due_after_str:
                    try:
                        filter_due_after = date.fromisoformat(due_after_str)
                    except ValueError:
                        print("Invalid date format. Ignoring due date after filter.")

            tasks = task_service.filter_tasks(
                completed=filter_completed,
                priority=filter_priority,
                tags=filter_tags,
                due_before=filter_due_before,
                due_after=filter_due_after
            )

            if not tasks:
                print("\nNo tasks matching the filter criteria.")
            else:
                sort_choice = input("Sort tasks by (title, priority, due_date, none) [none]: ").lower()
                if sort_choice in ["title", "priority", "due_date"]:
                    tasks = task_service.sort_tasks(sort_by=sort_choice)
                elif sort_choice != "none":
                    print("Invalid sort option. Not sorting tasks.")

                print("\n--- Your Filtered Tasks ---")
                for task in tasks:
                    status = "✓" if task.is_completed else " "
                    overdue_indicator = "[OVERDUE] " if task.is_overdue() else ""
                    priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(task.priority, "")
                    tags_str = f" ({', '.join(task.tags)})" if task.tags else ""
                    karachi_display_datetime = None
                    if task.due_date and task.due_time:
                        # Convert stored UTC datetime to Karachi for display
                        utc_datetime = datetime.combine(task.due_date, task.due_time, tzinfo=timezone.utc)
                        karachi_display_datetime = utc_datetime.astimezone(KARACHI_TIMEZONE)
                    elif task.due_date:
                        utc_datetime = datetime.combine(task.due_date, time(0,0,0), tzinfo=timezone.utc)
                        karachi_display_datetime = utc_datetime.astimezone(KARACHI_TIMEZONE)

                    due_date_str = f" Due: {karachi_display_datetime.strftime('%Y-%m-%d')}" if karachi_display_datetime else ""
                    due_time_str = f" @ {karachi_display_datetime.strftime('%I:%M %p')}" if karachi_display_datetime and task.due_time else ""
                    recurrence_str = f" (Rec: {task.recurrence_type})" if task.recurrence_type else ""
                    print(f"[{status}] {overdue_indicator}{priority_emoji} {task.title}{tags_str}{due_date_str}{due_time_str}{recurrence_str} (ID: {task.id})")
                print("---------------------------")

        elif choice == "3":
            task_id = input("Enter the ID of the task to update: ")
            existing_task = task_service.get_task(task_id)
            if not existing_task:
                print(f"\n❌ Task with ID '{task_id}' not found.")
                continue

            print(f"\n--- Update Task: '{existing_task.title}' ---")
            details_to_update = get_task_details_from_input(existing_task)
            
            try:
                task = task_service.update_task(task_id, **details_to_update)
                if task:
                    print(f"\n✅ Updated task: '{task.title}'")
                    notification_service.schedule_reminder(task)
                else:
                    print(f"\n❌ Task with ID '{task_id}' not found after update attempt.")
            except ValueError as e:
                print(f"\n❌ Error updating task: {e}")
        
        elif choice == "4":
            task_id = input("Enter the ID of the task to mark as complete: ")
            task = task_service.update_task(task_id, is_completed=True)
            if task:
                print(f"\n✅ Marked task as complete: '{task.title}'")
                notification_service.schedule_reminder(task)
            else:
                print(f"\n❌ Task with ID '{task_id}' not found.")
        
        elif choice == "5":
            task_id = input("Enter the ID of the task to delete: ")
            if task_service.delete_task(task_id):
                print("\n✅ Task deleted successfully.")
            else:
                print(f"\n❌ Task with ID '{task_id}' not found.")

        elif choice == "6":
            task_id = input("Enter the task ID: ")
            priority = input("Enter new priority (High, Medium, Low): ")
            try:
                task = task_service.update_task(task_id, priority=priority)
                if task:
                    print(f"\n✅ Set priority for task '{task.title}' to {priority}.")
                else:
                    print(f"\n❌ Task with ID '{task_id}' not found.")
            except ValueError as e:
                print(f"\n❌ Error setting priority: {e}")

        elif choice == "7":
            task_id = input("Enter the task ID: ")
            tags_input = input("Enter tags to add (space-separated): ")
            if tags_input:
                new_tags = tags_input.split()
                task = task_service.get_task(task_id)
                if task:
                    # Ensure tags are unique and don't duplicate existing ones
                    updated_tags = list(set(task.tags + new_tags))
                    task_service.update_task(task_id, tags=updated_tags)
                    print(f"\n✅ Added tags to task '{task.title}'.")
                else:
                    print(f"\n❌ Task with ID '{task_id}' not found.")
        
        elif choice == "8":
            keyword = input("Enter keyword to search: ")
            results = task_service.search_tasks(keyword)
            if not results:
                print(f"\nNo tasks found matching '{keyword}'.")
            else:
                print(f"\n--- Search Results for '{keyword}' ---")
                for task in results:
                    status = "✓" if task.is_completed else " "
                    overdue_indicator = "[OVERDUE] " if task.is_overdue() else ""
                    priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(task.priority, "")
                    tags_str = f" ({', '.join(task.tags)})" if task.tags else ""
                    karachi_display_datetime = None
                    if task.due_date and task.due_time:
                        # Convert stored UTC datetime to Karachi for display
                        utc_datetime = datetime.combine(task.due_date, task.due_time, tzinfo=timezone.utc)
                        karachi_display_datetime = utc_datetime.astimezone(KARACHI_TIMEZONE)
                    elif task.due_date:
                        utc_datetime = datetime.combine(task.due_date, time(0,0,0), tzinfo=timezone.utc)
                        karachi_display_datetime = utc_datetime.astimezone(KARACHI_TIMEZONE)

                    due_date_str = f" Due: {karachi_display_datetime.strftime('%Y-%m-%d')}" if karachi_display_datetime else ""
                    due_time_str = f" @ {karachi_display_datetime.strftime('%I:%M %p')}" if karachi_display_datetime and task.due_time else ""
                    recurrence_str = f" (Rec: {task.recurrence_type})" if task.recurrence_type else ""
                    print(f"[{status}] {overdue_indicator}{priority_emoji} {task.title}{tags_str}{due_date_str}{due_time_str}{recurrence_str} (ID: {task.id})")
                print("---------------------------------------")
        elif choice == "9":
            print("\n--- Processing Notifications ---")
            triggered = notification_manager.process_pending_notifications()
            if triggered:
                print(f"✅ Triggered {len(triggered)} notifications.")
            else:
                print("No pending notifications to trigger.")
        elif choice == "10":
            print("\n--- Sort Tasks ---")
            print("1. Title")
            print("2. Priority")
            print("3. Due Date")
            sort_choice = input("Choose sorting option: ")

            if sort_choice == "1":
                sorted_tasks = task_service.sort_tasks("title")
            elif sort_choice == "2":
                sorted_tasks = task_service.sort_tasks("priority")
            elif sort_choice == "3":
                sorted_tasks = task_service.sort_tasks("due_date")
            else:
                print("Invalid choice!")
                continue

            print("\n--- Sorted Tasks ---")
            for task in sorted_tasks:
                status = "✓" if task.is_completed else " "
                overdue_indicator = "[OVERDUE] " if task.is_overdue() else ""
                priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(task.priority, "")
                tags_str = f" ({', '.join(task.tags)})" if task.tags else ""
                karachi_display_datetime = None
                if task.due_date and task.due_time:
                    utc_datetime = datetime.combine(task.due_date, task.due_time, tzinfo=timezone.utc)
                    karachi_display_datetime = utc_datetime.astimezone(KARACHI_TIMEZONE)
                elif task.due_date:
                    utc_datetime = datetime.combine(task.due_date, time(0,0,0), tzinfo=timezone.utc)
                    karachi_display_datetime = utc_datetime.astimezone(KARACHI_TIMEZONE)

                due_date_str = f" Due: {karachi_display_datetime.strftime('%Y-%m-%d')}" if karachi_display_datetime else ""
                due_time_str = f" @ {karachi_display_datetime.strftime('%I:%M %p')}" if karachi_display_datetime and task.due_time else ""
                recurrence_str = f" (Rec: {task.recurrence_type})" if task.recurrence_type else ""
                print(f"[{status}] {overdue_indicator}{priority_emoji} {task.title}{tags_str}{due_date_str}{due_time_str}{recurrence_str} (ID: {task.id})")
            print("-------------------")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
