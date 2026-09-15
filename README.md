AI Study Planner

An AI-powered study planning application that helps students prioritize assignments, estimate workload, and create personalized study schedules.

The application combines a machine-learning workload prediction model, a weighted prioritization algorithm, and a dynamic scheduling system to help students decide what to work on and when.

Features:

1. AI Workload Prediction — Uses a scikit-learn Random Forest model to estimate assignment workload.
2. Smart Prioritization — Ranks assignments based on deadline urgency, workload, difficulty, and course importance.
3. Personalized Scheduling — Creates a study plan based on the number of hours available each day.
4. Priority Explanations — Shows why an assignment received its priority score.
5. Workload Analytics — Visualizes workload across courses.
6. Assignment Management — Add assignments directly through the application.
7. Automated Testing — Uses pytest to test prioritization and scheduling functionality.

Technology used:

1. Python
2. Streamlit
3. scikit-learn
4. pandas
5. JSON
6. CSV

Project Structure
AI-Study-Planner/
│
├── app.py                  # Streamlit application
├── planner.py              # Prioritization and scheduling logic
├── workload_model.py       # Machine-learning workload prediction
├── data.py                 # Assignment data management
│
├── assignments.json        # Assignment data
├── workload_history.csv    # Historical training data
├── requirements.txt        # Python dependencies

How to start:
1. Clone the repository
git clone https://github.com/Anishadate/AI-Study-Planner

2. Create a virtual environment

python3 -m venv .venv

3. Activate the virtual environment

macOS/Linux:

source .venv/bin/activate


Windows:

.venv\Scripts\activate


After activation, your terminal should show:

(.venv)

4. Install dependencies
python -m pip install -r requirements.txt

Run the Application

Start the Streamlit application with:

python -m streamlit run app.py


After running the command, Streamlit will provide a local URL like:

http://localhost:8501


Open that URL in your browser to use the application.

GitHub Codespaces

If running the project in GitHub Codespaces, Streamlit might automatically detect the application port.

If it does not, open the Ports tab in VS Code and forward port:

8501


Then open the forwarded URL.


How It Works:

The planner follows several steps:

Assignment Information
        ↓
ML Workload Prediction
        ↓
Priority Calculation
        ↓
Assignment Ranking
        ↓
Available Study Hours
        ↓
Personalized Study Schedule

Priority Calculation:

Assignments receive a score from 0–100 based on:

- 40% Deadline urgency
- 25% Estimated workload
- 20% Difficulty
- 15% Course importance

Higher-priority assignments are scheduled first.

Machine Learning:

The workload prediction model uses a Random Forest regression model from scikit-learn.

The model uses information such as:
1. Assignment difficulty
2. Course importance
3. Assignment type
4. Course
to estimate how many hours an assignment may require.

Historical workload data is stored in workload_history.csv.

Future Improvements

1. Automatically record actual time spent on assignments
2. Use completed assignments to improve future workload predictions
3. Add assignment completion tracking
4. Add calendar integration
5. Add study-session reminders
6. Improve scheduling around assignment deadlines
7. Add user accounts and persistent student profiles

Author:

Anisha Date
Computer Science student at the University of Minnesota — Twin Cities.