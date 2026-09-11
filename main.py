from planner import load_assignments, prioritize_assignments, create_schedule


def display_assignments(assignments):
    print("\n" + "=" * 60)
    print("              AI STUDY PLANNER")
    print("=" * 60)

    if not assignments:
        print("No assignments found.")
        return

    print("\nYOUR PRIORITIZED ASSIGNMENTS\n")

    for i, assignment in enumerate(assignments, start=1):
        print(f"{i}. {assignment['name']}")
        print(f"   Course:       {assignment['course']}")
        print(f"   Due:          {assignment['due']}")
        print(f"   Estimated:    {assignment['hours']} hours")
        print(f"   Difficulty:   {assignment['difficulty']}/5")
        print(f"   Priority:     {assignment['priority']}/100")
        print()


def display_schedule(schedule):
    print("\n" + "=" * 60)
    print("              RECOMMENDED STUDY PLAN")
    print("=" * 60)

    for day, tasks in schedule.items():
        print(f"\n{day}")
        print("-" * 40)

        if not tasks:
            print("  No study sessions scheduled.")
            continue

        for task in tasks:
            print(
                f"  • {task['name']} "
                f"({task['hours']} hrs) "
                f"[Priority: {task['priority']}]"
            )


def main():
    assignments = load_assignments("assignments.json")

    prioritized = prioritize_assignments(assignments)

    display_assignments(prioritized)

    schedule = create_schedule(prioritized)

    display_schedule(schedule)

    print("\nPlan generated successfully!")
    print("")


if __name__ == "__main__":
    main()