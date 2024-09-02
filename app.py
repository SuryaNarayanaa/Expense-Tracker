from flask import Flask, render_template, request, redirect, url_for ,send_file
import csv
from handle_csv import get_all_expenses, add_expense_to_db  ,delete_expense

app = Flask(__name__)

@app.route('/')
def index():
    expenses = get_all_expenses()
    return render_template('index.html', expenses=expenses)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    date = request.form.get('date')
    time = request.form.get('time')
    category = request.form.get('category')
    amount = request.form.get('amount')
    description = request.form.get('description')

    print(date, time, category, amount, description)

    add_expense_to_db(date, time, category, amount, description)
    return redirect(url_for('index'))



@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense_route(expense_id):
    delete_expense(expense_id)
    return redirect(url_for('index'))


@app.route('/download_csv')
def download_csv():
    csv_file_path = "expense.csv"
    
    
    
    return send_file(csv_file_path, as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)
