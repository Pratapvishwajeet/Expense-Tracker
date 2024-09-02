import json
from datetime import datetime
from collections import defaultdict
import tkinter as tk
from tkinter import messagebox, ttk

# File to store expenses
DATA_FILE = 'expenses.json'

# Load data from the JSON file
def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save data to the JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Add a new expense
def add_expense(amount, description, category):
    expense = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": amount,
        "description": description,
        "category": category
    }
    expenses = load_data()
    expenses.append(expense)
    save_data(expenses)
    messagebox.showinfo("Success", "Expense added successfully.")

# Show all expenses in a new window
def show_expenses():
    expenses = load_data()
    new_window = tk.Toplevel(root)
    new_window.title("All Expenses")
    new_window.geometry("600x400")
    new_window.configure(bg="#f5f5f5")

    tree = ttk.Treeview(new_window, columns=('Date', 'Amount', 'Description', 'Category'), show='headings', height=15)
    tree.heading('Date', text='Date', anchor='center')
    tree.heading('Amount', text='Amount', anchor='center')
    tree.heading('Description', text='Description', anchor='center')
    tree.heading('Category', text='Category', anchor='center')

    tree.column('Date', anchor='center', width=100)
    tree.column('Amount', anchor='center', width=100)
    tree.column('Description', anchor='center', width=200)
    tree.column('Category', anchor='center', width=150)

    for expense in expenses:
        tree.insert("", "end", values=(expense['date'], expense['amount'], expense['description'], expense['category']))

    tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Generate a monthly summary
def monthly_summary():
    month = month_entry.get()
    expenses = load_data()
    monthly_expenses = [exp for exp in expenses if exp['date'].startswith(month)]
    total = sum(exp['amount'] for exp in monthly_expenses)
    
    new_window = tk.Toplevel(root)
    new_window.title(f"Monthly Summary for {month}")
    new_window.geometry("400x300")
    new_window.configure(bg="#f5f5f5")

    summary_label = tk.Label(new_window, text=f"Total expenses for {month}: {total}", font=('Arial', 16, 'bold'), bg="#f5f5f5")
    summary_label.pack(pady=20)

    category_summary = defaultdict(float)
    for expense in monthly_expenses:
        category_summary[expense['category']] += expense['amount']

    category_text = "Category-wise breakdown:\n"
    for category, amount in category_summary.items():
        category_text += f"{category}: {amount}\n"

    category_label = tk.Label(new_window, text=category_text, font=('Arial', 14), bg="#f5f5f5")
    category_label.pack(pady=10)

# Show summary by category
def category_summary():
    expenses = load_data()
    category_expenses = defaultdict(float)
    for expense in expenses:
        category_expenses[expense['category']] += expense['amount']

    new_window = tk.Toplevel(root)
    new_window.title("Category Summary")
    new_window.geometry("400x300")
    new_window.configure(bg="#f5f5f5")

    summary_text = "Total expenses by category:\n"
    for category, amount in category_expenses.items():
        summary_text += f"{category}: {amount}\n"

    summary_label = tk.Label(new_window, text=summary_text, font=('Arial', 14), bg="#f5f5f5")
    summary_label.pack(pady=20)

# Function to handle adding an expense from the GUI
def handle_add_expense():
    try:
        amount = float(amount_entry.get())
        description = description_entry.get()
        category = category_entry.get()
        add_expense(amount, description, category)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for the amount.")

# Main GUI setup
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("500x600")
root.configure(bg="#f5f5f5")

# Title Label
title_label = tk.Label(root, text="Expense Tracker", font=('Arial', 24, 'bold'), bg="#f5f5f5", fg="#333")
title_label.pack(pady=20)

# Frame for input fields
input_frame = tk.Frame(root, bg="#f5f5f5")
input_frame.pack(pady=20)

# Input Fields
amount_label = tk.Label(input_frame, text="Amount:", font=('Arial', 16), bg="#f5f5f5")
amount_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
amount_entry = tk.Entry(input_frame, width=25, font=('Arial', 16))
amount_entry.grid(row=0, column=1, padx=10, pady=10)

description_label = tk.Label(input_frame, text="Description:", font=('Arial', 16), bg="#f5f5f5")
description_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
description_entry = tk.Entry(input_frame, width=25, font=('Arial', 16))
description_entry.grid(row=1, column=1, padx=10, pady=10)

category_label = tk.Label(input_frame, text="Category:", font=('Arial', 16), bg="#f5f5f5")
category_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
category_entry = tk.Entry(input_frame, width=25, font=('Arial', 16))
category_entry.grid(row=2, column=1, padx=10, pady=10)

# Frame for buttons
button_frame = tk.Frame(root, bg="#f5f5f5")
button_frame.pack(pady=30)

add_button = tk.Button(button_frame, text="Add Expense", font=('Arial', 16, 'bold'), command=handle_add_expense, width=20, bg="#4CAF50", fg="white")
add_button.grid(row=0, column=0, padx=10, pady=10)

show_button = tk.Button(button_frame, text="Show All Expenses", font=('Arial', 16, 'bold'), command=show_expenses, width=20, bg="#2196F3", fg="white")
show_button.grid(row=1, column=0, padx=10, pady=10)

month_label = tk.Label(button_frame, text="Month (YYYY-MM):", font=('Arial', 16), bg="#f5f5f5")
month_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
month_entry = tk.Entry(button_frame, width=20, font=('Arial', 16))
month_entry.grid(row=2, column=1, padx=10, pady=10)

summary_button = tk.Button(button_frame, text="Monthly Summary", font=('Arial', 16, 'bold'), command=monthly_summary, width=20, bg="#FF5722", fg="white")
summary_button.grid(row=3, column=0, padx=10, pady=10)

category_button = tk.Button(button_frame, text="Category Summary", font=('Arial', 16, 'bold'), command=category_summary, width=20, bg="#9C27B0", fg="white")
category_button.grid(row=4, column=0, padx=10, pady=10)

exit_button = tk.Button(button_frame, text="Exit", font=('Arial', 16, 'bold'), command=root.quit, width=20, bg="#f44336", fg="white")
exit_button.grid(row=5, column=0, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
