from datetime import date, timedelta

def get_next_recurrence_date(current_date: date, recurrence_type: str) -> date:
    """
    Calculates the next due date based on the current date and recurrence type.

    Args:
        current_date (date): The current due date of the task instance.
        recurrence_type (str): The type of recurrence ("Daily", "Weekly", "Monthly").

    Returns:
        date: The calculated next due date.

    Raises:
        ValueError: If an unsupported recurrence type is provided.
    """
    if recurrence_type == "Daily":
        return current_date + timedelta(days=1)
    elif recurrence_type == "Weekly":
        return current_date + timedelta(weeks=1)
    elif recurrence_type == "Monthly":
        next_month_day = current_date.day
        next_month_year = current_date.year
        next_month_month = current_date.month + 1

        if next_month_month > 12:
            next_month_month = 1
            next_month_year += 1
        
        # Try to create a date with the same day
        try:
            return date(next_month_year, next_month_month, next_month_day)
        except ValueError:
            # If the day does not exist in the next month (e.g., Feb 30th)
            # go to the last day of the next month
            last_day_of_next_month = (date(next_month_year, next_month_month + 1, 1) - timedelta(days=1)) \
                                     if next_month_month < 12 \
                                     else (date(next_month_year + 1, 1, 1) - timedelta(days=1))
            return last_day_of_next_month
    else:
        raise ValueError("Unsupported recurrence type. Must be 'Daily', 'Weekly', or 'Monthly'.")
