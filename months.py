import tkinter as tk
from tkinter import ttk
import expensetracker

def open_expense_tracker_window(expenses, selected_month):
    expensetracker.open_expense_tracker(root)

def select_month():
    selected_month = month_combobox.get()

    open_expense_tracker_window()

root = tk.Tk()
root.title('Month Selection')
root.geometry('400x300')

label = tk.Label(root, text='Select a month:', font=('Arial', 12))
label.pack(pady=10)

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
month_combobox = ttk.Combobox(root, values=months, font=('Arial', 12), state='readonly')
month_combobox.pack(pady=10)

select_button = tk.Button(root, text='Select', command=select_month, font=('Arial', 12))
select_button.pack(pady=10)

root.mainloop()

