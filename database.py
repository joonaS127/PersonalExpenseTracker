import sqlite3
import datetime
import time

# Connect to the SQLite database
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date DATE NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS monthly_budget (
    month TEXT PRIMARY KEY,
    budget REAL NOT NULL
)''')

conn.commit()
cursor.close()
conn.close()

# Function definitions
def fetch_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def fetch_expenses_by_month(selected_month):
    filtered_expenses = []
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    all_expenses = cursor.fetchall()

    for expense in all_expenses:
        expense_date = datetime.datetime.strptime(expense[4], "%Y-%m-%d")
        expense_month = expense_date.strftime("%B")
        if expense_month == selected_month:
            filtered_expenses.append(expense)

    conn.close()
    return filtered_expenses

def insert_expense(id, amount, category, description, date_str):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    cursor.execute('INSERT INTO expenses (id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)',
                   (id, amount, category, description, date))
    conn.commit()
    conn.close()

def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def update_expense(new_amount, new_category, new_description, new_date, id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE expenses SET amount = ?, category = ?, description = ?, date = ? WHERE id = ?", 
                   (new_amount, new_category, new_description, new_date, id))
    conn.commit()
    conn.close()

def set_monthly_budget(month, budget):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO monthly_budget (month, budget)
                   VALUES (?, ?)
                   ON CONFLICT(month) DO UPDATE SET budget = EXCLUDED.budget
                   ''', (month, budget))
    conn.commit()
    conn.close()

def update_monthly_budget(month, budget):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE monthly_budget SET budget = ? WHERE month = ?', (budget, month))
    conn.commit()
    conn.close()

def get_monthly_budget(month):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT budget FROM monthly_budget WHERE month = ?", (month,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

    