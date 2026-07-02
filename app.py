from flask import Flask, render_template, request, url_for, redirect, flash, Response
from flask_sqlalchemy import SQLAlchemy 
from datetime import date, datetime
from sqlalchemy import func


app = Flask(__name__)

app.secret_key = "any_random_string_you_want"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#helper function for date parse
def parse_date_or_none(s:str):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(120))
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)

with app.app_context():
    db.create_all()


CATEGORIES = ["Grocery", "Utilities", "Health", "Others"]
@app.route("/")
def index():
    start_str = (request.args.get("start", "")).strip()
    end_str = (request.args.get("end", "")).strip()
    selected_category = (request.args.get("category") or "").strip()
   
    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)

    if start_date and end_date and end_date < start_date:
        print(end_date < start_date)
        flash("End date can not be before start date", "error")
        start_date = end_date = None
        start_str = end_str = ""

    query = Expense.query
    
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)

    if selected_category:
        query = query.filter(Expense.category == selected_category)
        
    expenses = query.order_by(Expense.date.desc()).all()

    total_spent = round(sum(e.amount for e in expenses), 2)


# pie chart

    cat_q = db.session.query(Expense.category, func.sum(Expense.amount))
    
    if start_date:
        cat_q = cat_q.filter(Expense.date >= start_date)
    
    if end_date:
        cat_q = cat_q.filter(Expense.date <= end_date)

    if selected_category:
        cat_q = cat_q.filter(Expense.category == selected_category)
    
    cat_row = cat_q.group_by(Expense.category).all()
    cat_labels = [c for c, _ in cat_row]
    cat_values = [round(float(s or 0), 2) for _, s in cat_row]

# day chart
    day_q = db.session.query(Expense.date, func.sum(Expense.amount))
    
    if start_date:
        day_q = day_q.filter(Expense.date >= start_date)
    
    if end_date:
        day_q = day_q.filter(Expense.date <= end_date)

    if selected_category:
        day_q = day_q.filter(Expense.category == selected_category)
    
    day_row = day_q.group_by(Expense.date).order_by(Expense.date).all()
    day_labels = [d.isoformat() for d, _ in day_row]
    day_values = [round(float(s or 0), 2) for _, s in day_row]


    return render_template(
                            "index.html", 
                            expenses=expenses,
                            today=date.today().isoformat(),
                            categories=CATEGORIES, 
                            total_spent=total_spent, 
                            start_str=start_str, 
                            end_str=end_str,
                            selected_category=selected_category,
                            cat_labels = cat_labels,
                            cat_values=cat_values,
                            day_labels=day_labels,
                            day_values=day_values
                            )

@app.route("/add", methods = ["POST"])
def add():
    
    print(dict(request.form))
    # 1. extract data from the form
    description = request.form.get('description')
    amount_str = request.form.get('amount')
    category = request.form.get('category')
    date_str = request.form.get("date")

    # 2.validate and convert the data
    if not amount_str or not category:
        return "Amount and category are required", 400
    try:
        amount = float(amount_str)
    except ValueError:
        return "Amount must be a valid number", 400
    
    if date_str:
        expense_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        expense_date = date.today()
    
    # 3.create new expense object

    new_expense = Expense(
        description = description,
        amount = amount,
        category = category,
        date = expense_date
    )

    #save it to database
    db.session.add(new_expense)
    db.session.commit()

    return redirect(url_for("index"))

# delete route
@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    try:
        db.session.delete(expense)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "There is an error deleting the expense", 400
    

@app.route("/export.csv")
def export_csv():
    #1 read query string

    start_str = (request.args.get("start") or "").strip()
    end_str = (request.args.get("category") or "").strip()
    selected_category = (request.args.get("category") or "").strip()

    #2 parsing

    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)

    q = Expense.query
    
    if start_date:
        q = q.filter(Expense.date >= start_date)

    if end_date:
        q = q.filter(Expense.date <= end_date)
    
    if selected_category:
        q = q.filter(Expense.category == selected_category)

    expenses = q.order_by(Expense.date, Expense.id).all()
    

    lines = ["date, description, category, amount"]

    for e in expenses:
        lines.append(f"{e.date.isoformat()}, {e.description}, {e.category}, {e.amount:.2f}")
    
    csv_data = "\n".join(lines)

    fname_start = start_str or "all"
    fname_end = end_str or "all"
    filename = f"expenses_{fname_start}_to_{end_date}.csv"

    return Response(
        csv_data,
        headers={
            "Content-Type":"text/csv",
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


if __name__ == "__main__":
    app.run(debug=True)