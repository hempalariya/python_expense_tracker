# Python Expense Tracker

A simple web-based expense tracker built with Flask and SQLite. Add, edit, delete, filter, and export your expenses, with charts to visualize spending by category and over time.

## Features

- Add expenses with description, amount, category, and date
- Edit or delete existing expenses
- Filter expenses by date range and/or category
- View total spending for the current filter
- Export filtered expenses to CSV
- Visualize spending with a category pie chart and a spending-over-time bar chart (Chart.js)
- Categories: Grocery, Utilities, Health, Others

## Tech Stack

- [Flask](https://flask.palletsprojects.com/) — web framework
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) — ORM / SQLite storage
- [Tailwind CSS](https://tailwindcss.com/) (via CDN) — styling
- [Chart.js](https://www.chartjs.org/) (via CDN) — charts

## Getting Started

### Prerequisites

- Python 3.10+

### Installation

```bash
git clone <repo-url>
cd python_expense_tracker
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

### Run the app

```bash
python app.py
```

The app will start at `http://127.0.0.1:5000/` and automatically create a local SQLite database (`expense.db`) on first run.

## Project Structure

```
python_expense_tracker/
├── app.py              # Flask app, routes, and database model
├── requirements.txt    # Python dependencies
├── templates/
│   ├── layout.html     # Base layout (Tailwind + Chart.js)
│   ├── index.html      # Dashboard: filters, add form, table, charts
│   └── edit.html       # Edit expense form
└── instance/
    └── expense.db      # SQLite database (created automatically)
```

## Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Dashboard with filters, totals, expense table, and charts |
| `/add` | POST | Add a new expense |
| `/edit/<expense_id>` | GET, POST | Edit an existing expense |
| `/delete/<expense_id>` | POST | Delete an expense |
| `/export.csv` | GET | Export filtered expenses as a CSV file |

## Demo
<img width="1920" height="1032" alt="Screenshot 2026-07-04 123110" src="https://github.com/user-attachments/assets/20fe52c7-edeb-48b1-9767-fbe0579af4f2" />
<img width="1920" height="1032" alt="Screenshot 2026-07-04 123126" src="https://github.com/user-attachments/assets/3ab0910c-671b-470c-825e-91b4203042f5" />
<img width="1920" height="1032" alt="Screenshot 2026-07-04 123116" src="https://github.com/user-attachments/assets/da8f5eb2-6ef4-4c98-864d-320116183f52" />

