# AI-Study-Planner
A Python-based study planning tool that prioritizes assignments based on deadline urgency, difficulty, estimated workload, and course importance.

Overview
College students often have multiple assignments competing for their attention. The AI Study Planner helps determine which assignments should be completed first and creates a simple recommended study schedule.

The project uses a weighted prioritization algorithm to assign each task a score from 0–100.

Features
1. Tracks assignment deadlines
2. Considers estimated completion time
3. Calculates assignment priority
4. Uses a weighted decision-making algorithm
5. Considers course importance and difficulty
6. Generates a recommended study schedule
7. Uses JSON for simple data storage
8. 
How It Works
Each assignment receives a priority score based on four factors:

Factor	Weight
Deadline urgency	45%
Difficulty	25%
Estimated workload	20%
Course importance	10%
The final priority score is calculated using:

Priority =
    Urgency × 0.45
  + Difficulty × 0.25
  + Workload × 0.20
  + Importance × 0.10
Assignments are then sorted from highest to lowest priority.

Planned improvements include:

 Add a graphical user interface
 Add an interactive assignment entry system
 Store completed assignments
 Analyze historical study data
 Use machine learning to predict assignment completion time
 Add calendar integration
 Build a web version
 Add visualizations for workload by course
What I Learned
Through this project, I practiced working with structured data, functions, sorting algorithms, file handling, date calculations, and weighted decision-making.

I also explored how an algorithm can turn multiple inputs into a useful recommendation for a real-world problem.

Author
Anisha Date

Computer Science Student
University of Minnesota — Twin Cities
