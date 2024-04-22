import sqlite3
import datetime
import time


conn = sqlite3.connect('expenses.db')

# Creating a cursor object to execute SQL statements
cursor = conn.cursor()

# Create the expenses table
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
               id INTEGER PRIMARY KEY,
               amount REAL NOT NULL,
               category TEXT NOT NULL,
               description TEXT,
               date DATE NOT NULL
)''')

# Create the monthly expense table

cursor.execute('''CREATE TABLE IF NOT EXISTS monthly_budget (
               month TEXT PRIMARY KEY,
               budget REAL NOT NULL
             )
''')


conn.commit()
cursor.close()
conn.close()

def fetch_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def fetch_expenses_by_month(selected_month):
    filtered_expenses = []

    try:
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM expenses")
        all_expenses = cursor.fetchall()

        for expense in all_expenses:
            expense_date = datetime.datetime.strptime(expense[4], "%Y-%m-%d")
            expense_month = expense_date.strftime("%B")
            if expense_month == selected_month:
                filtered_expenses.append(expense)

    except Exception as e:
        print("Error fetching expenses:", e)

    finally:
        conn.close()

    print(len(filtered_expenses), "filtered expenses")

    return filtered_expenses


def insert_expense(id, amount, category, description, date_str):
    while True:
        try:
            conn = sqlite3.connect('expenses.db')
            cursor = conn.cursor()

            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

            cursor.execute('INSERT INTO expenses (id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)',
                           (id, amount, category, description, date))
            conn.commit()
            conn.close()
            break
        except sqlite3.IntegrityError as e:
            if e.args[0] == 'UNIQUE constraint failed: expenses.id':
                print("Duplicate id:", id)
            else:
                print("Other error:", e)
            time.sleep(0.5)

    print("Inserted new expense!")

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
    