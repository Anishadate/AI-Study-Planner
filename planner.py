from datetime import datetime, date


def calculate_days_remaining(due_date):
    """Return the number of days until an assignment is due."""

    today = date.today()
    due = datetime.strptime(due_date, "%Y-%m-%d").date()

    return (due - today).days


def calculate_urgency(due_date):
    """Calculate deadline urgency on a 0-100 scale."""

    days_remaining = calculate_days_remaining(due_date)

    if days_remaining <= 0:
        return 100
    elif days_remaining == 1:
        return 95
    elif days_remaining <= 3:
        return 85
    elif days_remaining <= 7:
        return 70
    elif days_remaining <= 14:
        return 50
    else:
        return 25


def calculate_priority(assignment):
    """
    Calculate assignment priority using a weighted scoring algorithm.

    Factors:
    - Deadline urgency: 40%
    - Estimated workload: 25%
    - Difficulty: 20%
    - Course importance: 15%
    """

    urgency = calculate_urgency(assignment["due"])

    difficulty = assignment["difficulty"] * 20

    workload = min(assignment["hours"] * 10, 100)

    importance = assignment.get("importance", 3) * 20

    priority = (
        urgency * 0.40
        + workload * 0.25
        + difficulty * 0.20
        + importance * 0.15
    )

    return round(min(priority, 100))


def explain_priority(assignment):
    """Return human-readable reasons for an assignment's priority."""

    reasons = []

    days_remaining = calculate_days_remaining(assignment["due"])

    if days_remaining <= 0:
        reasons.append("Due today or overdue")
    elif days_remaining == 1:
        reasons.append("Due tomorrow")
    elif days_remaining <= 3:
        reasons.append("Deadline is approaching")

    if assignment["difficulty"] >= 4:
        reasons.append("High difficulty")

    if assignment["hours"] >= 4:
        reasons.append("Large estimated workload")

    if assignment.get("importance", 3) >= 4:
        reasons.append("High course importance")

    if not reasons:
        reasons.append("Moderate deadline and workload")

    return reasons


def prioritize_assignments(assignments):
    """Calculate priorities and sort assignments highest to lowest."""

    prioritized = []

    for assignment in assignments:
        assignment = assignment.copy()
        assignment["priority"] = calculate_priority(assignment)
        prioritized.append(assignment)

    return sorted(
        prioritized,
        key=lambda x: x["priority"],
        reverse=True
    )


def create_schedule(assignments, available_hours=3):
    """
    Create a study schedule based on available hours per day.

    Assignments are scheduled according to priority.
    Large assignments can be split across multiple days.
    """

    if available_hours <= 0:
        raise ValueError("Available hours must be greater than zero.")

    schedule = {}
    remaining = [
        {
            **assignment,
            "remaining_hours": float(assignment["hours"])
        }
        for assignment in assignments
    ]

    for day_offset in range(7):

        current_day = date.today()

        # Add the current day to the schedule.
        from datetime import timedelta

        day = current_day + timedelta(days=day_offset)

        if day_offset == 0:
            day_name = "Today"
        elif day_offset == 1:
            day_name = "Tomorrow"
        else:
            day_name = day.strftime("%A, %b %d")

        schedule[day_name] = []

        hours_left = float(available_hours)

        for assignment in remaining:

            if hours_left <= 0:
                break

            if assignment["remaining_hours"] <= 0:
                continue

            session_hours = min(
                assignment["remaining_hours"],
                hours_left
            )

            schedule[day_name].append({
                "name": assignment["name"],
                "course": assignment.get("course", ""),
                "hours": round(session_hours, 1),
                "priority": assignment["priority"]
            })

            assignment["remaining_hours"] -= session_hours
            hours_left -= session_hours

    return schedule