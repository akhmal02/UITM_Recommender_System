# 🎓 CourseRec — UiTM Intelligent Course & Timetable Recommendation System

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/Database-MySQL%208.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Security](https://img.shields.io/badge/Auth-Bcrypt%20Hashing-orange?style=for-the-badge)](https://en.wikipedia.org/wiki/Bcrypt)
[![Domain](https://img.shields.io/badge/Domain-Higher%20Education%20Advising-blueviolet?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-Academic%20Project-green?style=for-the-badge)](LICENSE)

> **CourseRec (UiTM Recommender System)** is a full-stack academic advisement and planning platform built for university students at **Universiti Teknologi MARA (UiTM)**. Powered by a **7-Rule Match Recommendation Engine**, it analyzes individual student career aspirations, difficulty tolerances, and credit-hour constraints to deliver ranked course suggestions with transparent score justifications, automated clash-free timetable synthesis, and an interactive conversational academic advisor chatbot.

---

## 📌 Problem Background & Academic Context

Every semester, undergraduate students encounter significant decision paralysis during course registration periods:
* **Curriculum Navigation Overload:** Manually verifying prerequisites, faculty elective lists, and specialization tracks across hundred-page academic handbooks.
* **Timetable Scheduling Clashes:** Building a conflict-free lecture and tutorial schedule without overlapping time slots.
* **Lack of Transparent Guidance:** Standard portals offer course listings without contextual advice explaining *why* an elective fits a student's specific career goals.

**CourseRec** solves these challenges by providing:
* **Preference-Driven Profiling:** Captures desired fields (e.g., Software Engineering, AI & Data Science, Cybersecurity), target difficulty, learning formats, and workload capacity.
* **7-Rule Explainable Recommendation Engine:** Evaluates candidate courses across 7 distinct heuristic rules, providing clear percentage scores and reasoning for every suggestion.
* **Automated Timetable Generation:** Simulates student weekly schedules with instant clash detection and slot allocation.
* **Conversational Academic Advisor:** A knowledge-based chatbot trained on UiTM academic regulations, credit limits, and faculty guidelines.

---

## 🏗️ System Architecture & Recommendation Engine

```mermaid
flowchart TD
    Student([👤 Student / User]) --> Client[🖥️ Web Browser UI]
    
    subgraph Frontend ["Frontend Presentation (Glassmorphic Dock Menu)"]
        UI_Dash["Dashboard & Active Enrollments"]
        UI_Pref["Student Preference Questionnaire"]
        UI_Rec["Ranked Recommendation Feed"]
        UI_Table["Weekly Timetable View"]
        UI_Bot["Academic Advisor Chatbot"]
    end

    subgraph Backend ["⚙️ Flask Core Application (app.py)"]
        AuthService["Authentication (Bcrypt Hashing)"]
        RecEngine["7-Rule Match Recommendation Engine"]
        TimeEngine["Conflict-Free Timetable Generator"]
        ChatbotService["UiTM Knowledge-Based Advisor"]
    end

    subgraph Storage ["🗄️ MySQL Database (recsystem)"]
        T_Users[("users")]
        T_Prefs[("preferences")]
        T_Courses[("courses")]
        T_Enroll[("enrollments")]
    end

    Client --> Frontend
    Frontend --> Backend
    Backend --> Storage
    Storage --> RecEngine
    RecEngine -->|Ranked Matches + Justifications| UI_Rec
```

---

## 🧠 The 7-Rule Recommendation Engine

The engine scores every candidate course out of 100 points across seven weighted evaluation criteria:

| Rule | Evaluation Criteria | Description & Match Justification | Weight |
|---|---|---|:---:|
| **Rule 1** | **Primary Field Alignment** | Measures alignment with student's primary academic focus (e.g., Computing, AI, Web) | 25 pts |
| **Rule 2** | **Secondary Interest Overlap** | Awards points for multi-disciplinary electives matching secondary career keywords | 15 pts |
| **Rule 3** | **Difficulty & Prerequisite Fit** | Validates difficulty tolerance against course intensity rating | 15 pts |
| **Rule 4** | **Credit Load Balance** | Ensures course credit hours fit cleanly within remaining semester credit cap | 15 pts |
| **Rule 5** | **Delivery Format Preference** | Matches preferred learning modality (In-person lectures, Hybrid, or Online lab) | 10 pts |
| **Rule 6** | **Career Path Synergy** | Synergizes course learning outcomes with target industry competencies | 10 pts |
| **Rule 7** | **Popularity & Peer Rating** | Factored score based on peer enrollment velocity and completion feedback | 10 pts |

---

## 🗄️ Database Architecture (MySQL)

```mermaid
erDiagram
    USERS ||--o| PREFERENCES : configures
    USERS ||--o{ ENROLLMENTS : registers
    COURSES ||--o{ ENROLLMENTS : contains

    USERS {
        int id PK
        string username UK
        string email UK
        string password_hash
        datetime created_at
    }

    PREFERENCES {
        int id PK
        int user_id FK
        string primary_field
        string difficulty_level
        int max_credits
        string preferred_format
        text interest_tags
    }

    COURSES {
        int id PK
        string course_code UK
        string course_name
        string field
        string difficulty
        int credit_hours
        string format
        text description
    }

    ENROLLMENTS {
        int id PK
        int user_id FK
        int course_id FK
        datetime enrolled_at
    }
```

---

## 📂 Project Directory Structure

```text
UITM_Recommender_System/
├── README.md                      # Comprehensive system documentation
├── requirements.txt               # Top-level dependencies for quick setup
├── .gitignore                     # Excludes Python bytecode (__pycache__), local .env
└── recsystem/                     # Application source package
    ├── app.py                     # Flask server, URL routing & controllers
    ├── config.py                  # Environment variable configuration loader
    ├── config.env.example         # Template for MySQL connection parameters
    ├── database_schema.sql        # Relational schema DDL definitions
    ├── seed_courses.py            # Automated UiTM course catalog seeder script
    ├── uitm_knowledge.py          # Academic advisor knowledge base facts
    ├── models/
    │   └── db.py                  # MySQL connection pool manager
    ├── services/
    │   ├── auth.py                # Bcrypt authentication and session security
    │   ├── recommender.py         # 7-rule scoring and ranking algorithms
    │   ├── timetable.py           # Schedule conflict detection and planning
    │   └── chatbot.py             # Rule-based conversational academic assistant
    ├── static/                    # Stylesheets and JavaScript client handlers
    │   ├── css/style.css
    │   └── js/
    │       ├── app.js
    │       └── chatbot.js
    └── templates/                 # Jinja2 HTML templates with dock navigation
        ├── base.html              # Bottom dock master layout
        ├── dashboard.html         # Current enrollments and progress overview
        ├── preferences.html       # Student preference survey form
        ├── recommendations.html   # Ranked course recommendations with scores
        ├── courses.html           # Full searchable course catalog
        ├── timetable.html         # Interactive weekly schedule grid
        └── chatbot.html           # Embedded AI advising dialogue
```

---

## 🛠️ Step-by-Step Installation & Setup

### 1. Prerequisites
* **Python:** Version 3.9, 3.10, or 3.11 (`python --version`).
* **Database Server:** [MySQL Server 8.0+](https://dev.mysql.com/downloads/installer/) (or XAMPP MySQL).

### 2. Clone the Repository
```bash
git clone https://github.com/akhmal02/UITM_Recommender_System.git
cd UITM_Recommender_System
```

### 3. Create a Virtual Environment (Recommended)
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Initialize the MySQL Database
1. Open your MySQL client (MySQL Workbench, phpMyAdmin, or terminal CLI):
   ```bash
   mysql -u root -p
   ```
2. Create the database:
   ```sql
   CREATE DATABASE recsystem;
   ```
3. Import the initial database schema:
   ```bash
   mysql -u root -p recsystem < recsystem/database_schema.sql
   ```

### 6. Configure Environment Credentials
1. Copy the example configuration inside `recsystem`:
   ```bash
   cp recsystem/config.env.example recsystem/config.env
   ```
2. Open `recsystem/config.env` and update with your local MySQL credentials:
   ```env
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_NAME=recsystem
   DB_USER=root
   DB_PASS=your_actual_mysql_password
   SECRET_KEY=your_generated_secret_key
   ```

### 7. Seed Initial Course Catalog Data
Populate the database with official UiTM curriculum courses:
```bash
cd recsystem
python seed_courses.py
```

### 8. Run the Application
```bash
python app.py
```

Open your browser and navigate to:
```text
http://127.0.0.1:5000/
```

---

## 👨‍💻 Author & Academic Attribution
* **Developer:** Muhammad Akhmal bin Mohamad Hussin ([@akhmal02](https://github.com/akhmal02))
* **Institution:** Universiti Teknologi MARA (UiTM)
* **Faculty:** College of Computing, Informatics and Mathematics
* **Specialization:** Intelligent Systems & Web Application Engineering
