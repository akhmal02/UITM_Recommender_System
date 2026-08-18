# CourseRec — Course Recommendation System

A full-stack web application that recommends university courses using **user preferences** and **rule-based filtering**, built with Flask and MySQL.

## Features

- User registration and login (bcrypt password hashing)
- Preference management (field, difficulty, duration, format, credits, interests)
- 7-rule recommendation engine with match scoring and explanations
- Course catalog with filters and enrollment
- Modern white & geometric gray UI with bottom dock navigation
- Responsive design with smooth animations

## Project Structure

```
recsystem/
├── app.py                  # Flask application & routes
├── config.py               # Environment configuration
├── config.env              # Database credentials (local)
├── database_schema.sql     # MySQL schema + seed data
├── requirements.txt
├── models/
│   └── db.py               # MySQL connection
├── services/
│   ├── auth.py             # Authentication logic
│   └── recommender.py      # Rule-based recommendation engine
├── static/
│   ├── css/style.css
│   └── js/app.js
└── templates/
    ├── base.html           # Dock menu layout
    ├── index.html          # Landing page
    ├── login.html / signup.html
    ├── dashboard.html
    ├── preferences.html
    ├── recommendations.html
    ├── courses.html
    └── profile.html
```

## Setup

### 1. Install dependencies

```bash
cd recsystem
pip install -r requirements.txt
```

### 2. Configure MySQL

Copy `config.env.example` to `config.env` and set your MySQL credentials:

```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=recsystem
DB_USER=root
DB_PASS=your_password
SECRET_KEY=your-random-secret
```

### 3. Import database schema

```bash
mysql -u root -p < database_schema.sql
```

### 4. Run the application

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

## Rule-Based Filtering

| Rule | Description |
|------|-------------|
| 1 | Field of study must match |
| 2 | Difficulty within user level (+1 stretch max) |
| 3 | Duration preference scoring (Short/Medium/Long) |
| 4 | Delivery format preference |
| 5 | Credit limit enforcement |
| 6 | Interest tag overlap bonus |
| 7 | Student rating quality boost |

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL (PyMySQL)
- **Auth:** bcrypt, Flask sessions
- **Frontend:** HTML5, CSS3, vanilla JavaScript
