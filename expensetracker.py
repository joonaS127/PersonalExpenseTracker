import tkinter as tk
from tkinter import ttk, messagebox, END
import datetime
import database

window = None

def open_expense_tracker(root):

    global window 
    
    window = tk.Toplevel(root)
    window.title('Personal Expense Tracker')
    window.geometry('1000x500')
    window.config(bg='#f0f0f0')
    window.resizable(False, False)

font1 = ('Arial', 12)
font2 = ('Arial', 10)

# functions

def add_to_treeview():
    expenses = database.fetch_expenses()
    tree.delete(*tree.get_children())
    for expense in expenses:
        tree.insert('', END, values = expense)

def insert():
    id = id_entry.get()
    amount = amount_entry.get()
    category = category_combobox.get()
    description = desc_entry.get()
    date = date_combobox.get()
    if not (id and amount and category and description and date):
        messagebox.showerror('Error', 'Please enter all fields')
   
    else:
        database.insert_expense(id, amount, category, description, date)
        add_to_treeview()
        messagebox.showinfo('Data successfully inserted')

def clear():
        tree.selection_remove(tree.focus())
        id_entry.delete(0,END)
        amount_entry.delete(0,END)
        category_combobox.set('')
        desc_entry.delete(0,END)
        date_combobox.set('')

def delete():
    selected_expense = tree.focus()
    if not selected_expense:
        messagebox.showerror('Error', 'Choose an expense to delete!')
    else:
        id = id_entry.get()
        database.delete_expense(id)
        add_to_treeview()
        clear()
        messagebox.showinfo('Success', 'Expense successfully deleted!')

def update():
    selected_expense = tree.focus()
    if not selected_expense:
        messagebox.showerror('Error', 'Choose an expense to update!')
    else:
        id = id_entry.get()
        amount = amount_entry.get()
        category = category_combobox.get()
        description = desc_entry.get()
        date = date_combobox.get()
        database.update_expense(amount, category, description, date, id)
        add_to_treeview()
        clear()
        messagebox.showinfo('Success', 'Expense updated successfully!')

def display_data(event):
    item_id = tree.identify_row(event.y)  # Get the item ID based on the mouse click position
    if item_id:
        row = tree.item(item_id)['values']
        clear()  # Clear the entries before populating with new data
        id_entry.insert(0, row[0])
        amount_entry.insert(0, row[1])
        category_index = categories.index(row[2]) if row[2] in categories else 0
        category_combobox.current(category_index)
        desc_entry.insert(0, row[3])
        date_combobox.set(row[4])
    else:
        clear()


# Labels
labels = ['ID:', 'Amount:', 'Category:', 'Description:', 'Date:']
for i, label_text in enumerate(labels):
    label = tk.Label(window, text=label_text, font=font1, bg='#f0f0f0')
    label.grid(row=i, column=0, padx=10, pady=5, sticky='w')

# Entries
id_entry = ttk.Entry(window, font=font1)
id_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

amount_entry = ttk.Entry(window, font=font1)
amount_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

categories = ['Food', 'Transport', 'Leisure', 'Clothing', 'Other']
category_combobox = ttk.Combobox(window, font=font1, values=categories, state='readonly')
category_combobox.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

desc_entry = ttk.Entry(window, font=font1)
desc_entry.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

current_date = datetime.date.today()
dates = [current_date - datetime.timedelta(days=i) for i in range(10)]  # Example: Last 10 days
date_values = [current_date.strftime('%Y-%m-%d')] + [date.strftime('%Y-%m-%d') for date in dates]
date_combobox = ttk.Combobox(window, font=font1, values=date_values, state='readonly')
date_combobox.grid(row=4, column=1, padx=10, pady=5, sticky='ew')
date_combobox.current(0)  # Set the current day as default

style = ttk.Style(window)

style.theme_use('clam')
style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837')
style.map('Treeview', background=[('selected', '1#A8F2D')])

tree = ttk.Treeview(window)

tree['columns'] = ('ID', 'Amount', 'Category', 'Description', 'Date')

tree.column('#0', width=0, stretch=tk.NO)  # Hide the default first column
tree.column('ID', anchor=tk.CENTER, width=120)
tree.column('Amount', anchor=tk.CENTER, width=120)
tree.column('Category', anchor=tk.CENTER, width=120)
tree.column('Description', anchor=tk.CENTER, width=120)
tree.column('Date', anchor=tk.CENTER, width=120)

tree.heading('ID', text='ID')
tree.heading('Amount', text='Amount')
tree.heading('Category', text='Category')
tree.heading('Description', text='Description')
tree.heading('Date', text='Date')

# Adjust placement and size of the treeview
tree.grid(row=0, column=2, rowspan=5, padx=10, pady=5, sticky='nsew')

# Buttons
add_btn = tk.Button(window, command=insert, text='Add expense', font=font1, fg='#fff', bg='#05A312', activebackground='#00850B', cursor='hand2', width=15, bd=0)
add_btn.grid(row=5, column=0, padx=10, pady=5)

delete_btn = tk.Button(window, command=delete, text='Delete expense', font=font1, fg='#fff', bg='#05A312', activebackground='#00850B', cursor='hand2', width=15, bd=0)
delete_btn.grid(row=5, column=1, padx=10, pady=5)

update_btn = tk.Button(window, command=update, text='Update expense', font=font1, fg='#fff', bg='#05A312', activebackground='#00850B', cursor='hand2', width=15, bd=0)
update_btn.grid(row=5, column=2, padx=10, pady=5)

tree.bind('<ButtonRelease>', display_data)

add_to_treeview()

window.mainloop()



