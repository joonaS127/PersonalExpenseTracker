import sqlite3

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

def insert_expense(id, amount, category, description, date):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
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
    