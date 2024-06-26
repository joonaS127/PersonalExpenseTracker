import tkinter as tk
from tkinter import ttk, messagebox, END
import datetime
import database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import collections

is_displaying_data = False
recursive_call_count = 0  # Define the recursive call count variable
last_selected_item = None
MAX_RECURSIVE_CALLS = 10

def open_expense_tracker_window(selected_month):
    global recursive_call_count  # Access the global variable
    expenses = database.fetch_expenses_by_month(selected_month)
    window = tk.Toplevel()
    window.title(f'Expense Tracker - {selected_month}')
    window.geometry('1000x380')
    window.config(bg='#f0f0f0')
    window.resizable(False, False)

    font1 = ('Arial', 12)
    font2 = ('Arial', 10)

    global tree, id_entry, amount_entry, category_combobox, desc_entry, date_combobox

    # Declare global variables
    tree = None
    id_entry = None
    amount_entry = None
    category_combobox = None
    desc_entry = None
    date_combobox = None

    # Functions
    def add_to_treeview(expenses):
        tree.delete(*tree.get_children())
        for expense in expenses:
            tree.insert('', END, values=expense)

    def insert():
        global tree, id_entry, amount_entry, category_combobox, desc_entry, date_combobox
        id_val = id_entry.get()
        amount_val = amount_entry.get()
        category_val = category_combobox.get()
        description_val = desc_entry.get()
        date_val = date_combobox.get()
        if not (id_val and amount_val and category_val and description_val and date_val):
            messagebox.showerror('Error', 'Please enter all fields')
        else:
            database.insert_expense(id_val, amount_val, category_val, description_val, date_val)
            add_to_treeview(database.fetch_expenses_by_month(selected_month))

    def clear():
        id_entry.delete(0, END)
        amount_entry.delete(0, END)
        category_combobox.set('')
        desc_entry.delete(0, END)
        date_combobox.set('')

    def clear_the_selection():
        tree.selection_remove(tree.focus())
        id_entry.delete(0, END)
        amount_entry.delete(0, END)
        category_combobox.set('')
        desc_entry.delete(0, END)
        date_combobox.set('')


    def delete():
        selected_expense = tree.focus()
        if not selected_expense:
            messagebox.showerror('Error', 'Choose an expense to delete!')
        else:
            id_val = tree.item(selected_expense)['values'][0]
            database.delete_expense(id_val)
            add_to_treeview(database.fetch_expenses_by_month(selected_month))
            clear()

    def update():
        selected_expense = tree.focus()
        if not selected_expense:
            messagebox.showerror('Error', 'Choose an expense to update!')
        else:
            id_val = id_entry.get()
            amount_val = amount_entry.get()
            category_val = category_combobox.get()
            description_val = desc_entry.get()
            date_val = date_combobox.get()
            database.update_expense(amount_val, category_val, description_val, date_val, id_val)
            add_to_treeview(database.fetch_expenses_by_month(selected_month))

  

    def display_data(event):
       global last_selected_item
           
       print("Displaying data...")
       print("Recursive call count:", recursive_call_count)
       print("Event:", event)
       print("Tree focus:", tree.focus())
       print("Tree children:", tree.get_children())

    
       item_id = tree.focus()

       if item_id and item_id != last_selected_item:
       
          last_selected_item = item_id

          tree.selection_set(item_id)

          row = tree.item(item_id)['values']
    
          clear()
          print("Tree item:", tree.item(item_id))
           
          print("This is the row", row)
          id_entry.insert(0, row[0])
          amount_entry.insert(0, row[1])
          category_index = categories.index(row[2]) if row[2] in categories else 0
          category_combobox.current(category_index)
          desc_entry.insert(0, row[3])
          date_combobox.set(row[4])
       elif not item_id:
           clear()

    def show_chart(selected_month):
    # Fetch expenses and create a pie chart
       expenses = database.fetch_expenses_by_month(selected_month)
       category_count = collections.Counter(expense[2] for expense in expenses)

       fig, ax = plt.subplots()
       ax.pie(category_count.values(), labels=category_count.keys(), autopct='%1.1f%%', startangle=90)
       ax.axis('equal')

    # Create a new window for the chart
       chart_window = tk.Toplevel()
       chart_window.title("Monthly Expenses")
       chart_window.geometry("400x450")  # Ensure the window is tall enough

    # Embed the pie chart in the window
       canvas = FigureCanvasTkAgg(fig, master=chart_window)
       canvas.draw()
       canvas.get_tk_widget().pack(pady=10)  # Ensure padding for the chart

    # Get the monthly budget
       monthly_budget = database.get_monthly_budget(selected_month)

    # Get the total expenses for the month
       total_expenses = database.get_total_expenses_for_month(selected_month)
       print("TOTAL EXPENSES: ", total_expenses)

       if monthly_budget is not None:
           remaining_budget = monthly_budget - total_expenses
           budget_text = f"Remaining budget for {selected_month}: ${remaining_budget:.2f}"
       else:
           budget_text = "No budget set for this month"

       budget_label = tk.Label(chart_window, text=budget_text, font=("Arial", 12))
       budget_label.pack(pady=10)  # Ensure padding for the budget label

       
    # Labels
    labels = ['ID:', 'Amount:', 'Category:', 'Description:', 'Date:']
    for i, label_text in enumerate(labels):
        label = tk.Label(window, text=label_text, font=font1, bg='#f0f0f0')
        label.grid(row=i, column=0, padx=25, pady=5, sticky='ws')

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
    style.map('Treeview', background=[('selected', 'blue')])

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
    tree.grid(row=0, column=2, rowspan=12, padx=10, pady=5, sticky='ns')

    tree.bind('<<TreeviewSelect>>', display_data)

    recursive_call_count = 0

    # Buttons
    add_btn = tk.Button(window, command=insert, text='Add expense', font=font1, fg='#fff', bg='#00ff00',
                        activebackground='#00cc00', cursor='hand2', width=15, bd=0)
    add_btn.grid(row=6, column=0, padx=10, pady=10)

    delete_btn = tk.Button(window, command=delete, text='Delete expense', font=font1, fg='#000000', bg='#ff0000',
                           activebackground='#cc0000', cursor='hand2', width=15, bd=0)
    delete_btn.grid(row=7, column=0, padx=10, pady=10)

    update_btn = tk.Button(window, command=update, text='Update expense', font=font1, fg='#fff', bg='#00ff00',
                           activebackground='#00cc00', cursor='hand2', width=15, bd=0)
    update_btn.grid(row=6, column=1, padx=10, pady=10)

    clear_all_btn = tk.Button(window, command=clear_the_selection, text='Clear entries', font=font1, fg='#000000', bg='#ffff00',
                        activebackground='#00cc00', cursor='hand2', width=15, bd=0)
    clear_all_btn.grid(row=7, column=1, padx=10, pady=10)

    chart_btn = tk.Button(window, text='Show Charts', font=font1, command=lambda: show_chart(selected_month))
    chart_btn.grid(row=12, column=2, padx=50, pady=15, sticky='w')

    set_budget_btn = tk.Button(window, text='Set Budget', font=font1, command=lambda: open_set_budget_window(selected_month))
    set_budget_btn.grid(row=12, column=2, padx=0, pady=15)

    add_to_treeview(expenses)

def select_month():
    selected_month = month_combobox.get()
    open_expense_tracker_window(selected_month)

root = tk.Tk()
root.title('Month Selection')
root.geometry('300x200')
root.resizable(False, False)

font = ('Arial', 12)

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
month_combobox = ttk.Combobox(root, font=font, values=months, state='readonly')
month_combobox.pack(pady=20)
month_combobox.current(0)

select_button = ttk.Button(root, text='Select Month', command=select_month)
select_button.pack()

def open_set_budget_window(selected_month):
    window = tk.Toplevel()
    window.title(f'Set Budget - {selected_month}')
    window.geometry('300x150')
    window.resizable(False, False)

    font = ('Arial', 12)

    budget_label = ttk.Label(window, text='Budget', font=font)
    budget_label.pack(pady=10)

    budget_entry = ttk.Entry(window, font=font)
    budget_entry.pack(pady=10)

    def clear_budget_entry():
        budget_entry.delete(0, END)

    def set_budget():
        budget = budget_entry.get()
        if budget.isnumeric():
            budget = float(budget)
            database.set_monthly_budget(selected_month, budget)
            messagebox.showinfo('Success', f'Budget set to {budget} for {selected_month}')
        else:
            messagebox.showerror('Error', 'Please enter a valid number for the budget')

    def update_budget():
        new_budget = budget_entry.get()
        if new_budget.isnumeric():
            new_budget = float(new_budget)
            database.update_monthly_budget(selected_month, new_budget)
            clear_budget_entry()
            messagebox.showinfo('Success', f'Budget updated to {new_budget} for {selected_month}')
        else:
            messagebox.showerror('Error', 'Please enter a valid number')

    # Create a frame to hold the buttons
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    # Buttons to Set and Update Budget
    set_budget_btn = ttk.Button(button_frame, text='Set Budget', command=set_budget)
    set_budget_btn.pack(side=tk.LEFT,  padx=5)

    update_budget_btn = ttk.Button(button_frame, text='Update Budget', command=update_budget)
    update_budget_btn.pack(side=tk.LEFT, padx=5)

root.mainloop()