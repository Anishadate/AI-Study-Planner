import json
from datetime import datetime


def load_assignments(filename):
    """Load assignments from a JSON file."""
    with open(filename, "r") as file:
        return json.load(file)


def calculate_urgency(due_date):
    """Calculate urgency based on how soon an assignment is due."""

    today = datetime.now().date()
    due = datetime.strptime(due_date, "%Y-%m-%d").date()

    days_remaining = (due - today).days

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
    - Deadline urgency: 45%
    - Difficulty: 25%
    - Estimated workload: 20%
    - Course importance: 10%
    """

    urgency = calculate_urgency(assignment["due"])

    difficulty = assignment["difficulty"] * 20

    workload = min(assignment["hours"] * 10, 100)

    importance = assignment.get("importance", 3) * 20

    priority = (
        urgency * 0.45
        + difficulty * 0.25
        + workload * 0.20
        + importance * 0.10
    )

    return round(priority)


def prioritize_assignments(assignments):
    """Calculate priorities and sort assignments from highest to lowest."""

    for assignment in assignments:
        assignment["priority"] = calculate_priority(assignment)

    return sorted(
        assignments,
        key=lambda x: x["priority"],
        reverse=True
    )


def create_schedule(assignments):
    """
    Create a simple study schedule.

    Higher-priority assignments are scheduled first.
    """

    schedule = {
        "Today": [],
        "Tomorrow": [],
        "This Week": []
    }

    for assignment in assignments:
        if assignment["priority"] >= 80:
            schedule["Today"].append(assignment)
        elif assignment["priority"] >= 60:
            schedule["Tomorrow"].append(assignment)
        else:
            schedule["This Week"].append(assignment)

    return schedule