import streamlit as st
import pandas as pd
from datetime import date

from data import (
    load_assignments,
    save_assignments
)

from planner import (
    prioritize_assignments,
    create_schedule,
    explain_priority
)

from workload_model import (
    train_workload_model,
    predict_workload
)


st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="wide"
)


# -----------------------------
# Styling
# -----------------------------

st.markdown(
    """
    <style>
    .main {
        background-color: #f7f8fc;
    }

    .priority-high {
        color: #d62728;
        font-weight: bold;
    }

    .priority-medium {
        color: #ff8c00;
        font-weight: bold;
    }

    .priority-low {
        color: #2ca02c;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Load data
# -----------------------------

assignments = load_assignments()

try:
    model = train_workload_model()
except Exception as error:
    model = None
    st.warning(
        f"ML model could not be loaded: {error}"
    )


# -----------------------------
# Header
# -----------------------------

st.title("📚 AI Study Planner")

st.markdown(
    """
    **Plan smarter. Prioritize what matters. Study with purpose.**

    The planner uses assignment characteristics, machine learning,
    deadline urgency, workload, difficulty, and course importance
    to create a personalized study plan.
    """
)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("⚙️ Study Settings")

available_hours = st.sidebar.number_input(
    "Available study hours per day",
    min_value=0.5,
    max_value=12.0,
    value=3.0,
    step=0.5
)


# -----------------------------
# Add assignment
# -----------------------------

st.sidebar.header("➕ Add Assignment")

with st.sidebar.form("assignment_form"):

    name = st.text_input("Assignment name")

    course = st.text_input("Course")

    due = st.date_input(
        "Due date",
        value=date.today()
    )

    difficulty = st.slider(
        "Difficulty",
        min_value=1,
        max_value=5,
        value=3
    )

    importance = st.slider(
        "Course importance",
        min_value=1,
        max_value=5,
        value=3
    )

    assignment_type = st.selectbox(
        "Assignment type",
        [
            "Homework",
            "Project",
            "Lab",
            "Reading",
            "Exam",
            "Quiz",
            "Other"
        ]
    )

    submitted = st.form_submit_button(
        "Add Assignment"
    )

    if submitted:

        if not name or not course:
            st.error(
                "Please enter both an assignment name and course."
            )

        else:

            new_assignment = {
                "name": name,
                "course": course,
                "due": due.strftime("%Y-%m-%d"),
                "difficulty": difficulty,
                "importance": importance,
                "assignment_type": assignment_type
            }

            if model:
                predicted_hours = predict_workload(
                    model,
                    new_assignment
                )
            else:
                predicted_hours = max(
                    1,
                    difficulty * 0.75
                )

            new_assignment["hours"] = predicted_hours

            assignments.append(new_assignment)

            save_assignments(assignments)

            st.success(
                f"Added assignment! Estimated workload: "
                f"{predicted_hours} hours."
            )

            st.rerun()


# -----------------------------
# Dashboard metrics
# -----------------------------

prioritized = prioritize_assignments(assignments)

total_hours = sum(
    assignment["hours"]
    for assignment in prioritized
)

high_priority = sum(
    assignment["priority"] >= 80
    for assignment in prioritized
)

upcoming = sum(
    assignment["priority"] >= 60
    for assignment in prioritized
)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📚 Assignments",
    len(prioritized)
)

col2.metric(
    "⏱ Total Workload",
    f"{total_hours:.1f} hrs"
)

col3.metric(
    "🔥 High Priority",
    high_priority
)

col4.metric(
    "📅 Upcoming",
    upcoming
)


st.divider()


# -----------------------------
# Prioritized assignments
# -----------------------------

st.header("Prioritized Assignments")


if not prioritized:

    st.info(
        "No assignments yet. Add an assignment from the sidebar."
    )

else:

    for assignment in prioritized:

        priority = assignment["priority"]

        if priority >= 80:
            color = "🔴"
        elif priority >= 60:
            color = "🟠"
        else:
            color = "🟢"

        with st.expander(
            f"{color} {assignment['name']} — "
            f"Priority {priority}/100"
        ):

            col1, col2, col3, col4 = st.columns(4)

            col1.write(
                f"**Course**  \n"
                f"{assignment['course']}"
            )

            col2.write(
                f"**Due**  \n"
                f"{assignment['due']}"
            )

            col3.write(
                f"**Estimated workload**  \n"
                f"{assignment['hours']} hours"
            )

            col4.write(
                f"**Difficulty**  \n"
                f"{assignment['difficulty']}/5"
            )

            st.markdown("### Why is this priority?")

            reasons = explain_priority(assignment)

            for reason in reasons:
                st.write(f"• {reason}")


# -----------------------------
# Study schedule
# -----------------------------

st.divider()

st.header("📅 Personalized Study Plan")

schedule = create_schedule(
    prioritized,
    available_hours
)

for day, tasks in schedule.items():

    if not tasks:
        continue

    st.subheader(day)

    for task in tasks:

        st.write(
            f"**{task['name']}** — "
            f"{task['hours']} hrs "
            f"(Priority {task['priority']})"
        )


# -----------------------------
# Analytics
# -----------------------------

st.divider()

st.header("📊 Workload Analytics")

if prioritized:

    course_data = {}

    for assignment in prioritized:

        course = assignment["course"]

        course_data[course] = (
            course_data.get(course, 0)
            + assignment["hours"]
        )

    chart_data = pd.DataFrame(
        {
            "Course": list(course_data.keys()),
            "Hours": list(course_data.values())
        }
    )

    chart_data = chart_data.set_index("Course")

    st.bar_chart(chart_data)


# -----------------------------
# ML explanation
# -----------------------------

st.divider()

st.header("🤖 About the AI Model")

st.write(
    """
    The workload prediction model uses a Random Forest regression
    algorithm from scikit-learn. It learns from historical assignment
    data using assignment difficulty, course importance, assignment
    type, and course as input features.
    """
)

if model:
    st.success(
        "ML workload prediction model is active."
    )
else:
    st.warning(
        "The application is currently using a fallback workload estimate."
    )
