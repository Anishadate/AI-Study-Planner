import json
import os


ASSIGNMENTS_FILE = "assignments.json"


def load_assignments(filename=ASSIGNMENTS_FILE):
    """Load assignments from JSON."""

    if not os.path.exists(filename):
        return []

    with open(filename, "r") as file:
        return json.load(file)


def save_assignments(assignments, filename=ASSIGNMENTS_FILE):
    """Save assignments to JSON."""

    with open(filename, "w") as file:
        json.dump(assignments, file, indent=4)


def add_assignment(assignment, filename=ASSIGNMENTS_FILE):
    """Add a new assignment to the assignment database."""

    assignments = load_assignments(filename)

    assignments.append(assignment)

    save_assignments(assignments, filename)


def delete_assignment(index, filename=ASSIGNMENTS_FILE):
    """Delete an assignment by index."""

    assignments = load_assignments(filename)

    if index < 0 or index >= len(assignments):
        raise IndexError("Assignment index out of range.")

    assignments.pop(index)

    save_assignments(assignments, filename)
