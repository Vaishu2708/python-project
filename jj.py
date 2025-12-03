import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import matplotlib.pyplot as plt

# File to store transactions
file_path = "transactions.csv"

# Load transactions
def load_transactions():
    try:
        transactions = pd.read_csv(file_path)
        if transactions.empty:
            transactions = pd.DataFrame(columns=['Date', 'Type', 'Category', 'Amount'])
    except (FileNotFoundError, pd.errors.EmptyDataError):
        transactions = pd.DataFrame(columns=['Date', 'Type', 'Category', 'Amount'])
    return transactions

# Save transactions
def save_transactions(transactions):
    transactions.to_csv(file_path, index=False)

# Update categories dynamically
def update_categories(event=None):
    selected_type = type_var.get()
    categories = {
        "Income": ["Salary", "Freelance", "Bonus", "Other"],
        "Expense": ["Rent", "Groceries", "Utilities", "Entertainment", "Other"],
        "Investment": ["Stocks", "Crypto", "Real Estate", "Mutual Funds", "Other"]
    }
    category_dropdown["values"] = categories.get(selected_type, ["Other"])
    category_var.set(categories[selected_type][0])

# Add transaction
def add_transaction():
    type_ = type_var.get()
    category = category_var.get()
    amount = amount_var.get()
    date = datetime.now().strftime("%Y-%m-%d")

    if not type_ or not category or not amount:
        messagebox.showerror("Error", "Please fill out all fields.")
        return

    try:
        amount = float(amount)
        transactions = load_transactions()
        new_transaction = pd.DataFrame([[date, type_, category, amount]], 
                                       columns=['Date', 'Type', 'Category', 'Amount'])
        transactions = pd.concat([transactions, new_transaction], ignore_index=True)
        save_transactions(transactions)
        messagebox.showinfo("Success", "Transaction added successfully!")
        refresh_transactions()
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric amount.")

# Delete selected transaction
def delete_transaction():
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showerror("Error", "Please select a transaction to delete.")
        return

    transactions = load_transactions()
    transactions.drop(index=selected_index[0], inplace=True)
    transactions.reset_index(drop=True, inplace=True)
    save_transactions(transactions)

    messagebox.showinfo("Success", "Transaction deleted successfully!")
    refresh_transactions()

# Refresh transactions list and update summary
def refresh_transactions():
    transactions = load_transactions()
    listbox.delete(0, tk.END)

    total_income = transactions[transactions['Type'] == 'Income']['Amount'].sum()
    total_expense = transactions[transactions['Type'] == 'Expense']['Amount'].sum()
    total_investment = transactions[transactions['Type'] == 'Investment']['Amount'].sum()
    savings = total_income - total_expense - total_investment

    # Update UI
    for _, row in transactions.iterrows():
        listbox.insert(tk.END, f"{row['Date']} | {row['Type']} | {row['Category']} | ₹{row['Amount']:.2f}")

    # Display financial summary
    income_label.config(text=f"Total Income: {total_income:.2f}")
    expense_label.config(text=f"Total Expense: {total_expense:.2f}")
    investment_label.config(text=f"Total Investment: {total_investment:.2f}")
    savings_label.config(text=f"Savings: {savings:.2f}")

    # Budget Analysis
    try:
        budget_limit = float(budget_var.get())
        if total_expense > budget_limit:
            budget_status_label.config(text="Over Budget! ❌", fg="red")
        else:
            budget_status_label.config(text="Within Budget ✅", fg="green")
    except ValueError:
        budget_status_label.config(text="Set a valid budget!", fg="orange")

# Show summary graph
def show_graph():
    transactions = load_transactions()
    
    if transactions.empty:
        messagebox.showinfo("Graph", "No transactions available to display.")
        return
    
    grouped = transactions.groupby('Type')['Amount'].sum()
    
    plt.figure(figsize=(6, 4))
    plt.bar(grouped.index, grouped.values, color=['green', 'red', 'blue'])
    plt.xlabel("Transaction Type")
    plt.ylabel("Total Amount")
    plt.title("Income vs Expense vs Investment")
    plt.show()

# Exit Application
def exit_app():
    root.quit()
    root.destroy()

# Initialize GUI
root = tk.Tk()
root.title("Personal Finance Manager")
root.geometry("550x600")

# Labels
tk.Label(root, text="Type:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
tk.Label(root, text="Category:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
tk.Label(root, text="Amount (₹):").grid(row=2, column=0, sticky="w", padx=5, pady=5)

# Variables
type_var = tk.StringVar()
category_var = tk.StringVar()
amount_var = tk.StringVar()
budget_var = tk.StringVar(value="0.00")

# Dropdowns
type_dropdown = ttk.Combobox(root, textvariable=type_var, values=["Income", "Expense", "Investment"], state="readonly")
type_dropdown.grid(row=0, column=1, padx=5, pady=5)
type_dropdown.current(0)
type_dropdown.bind("<<ComboboxSelected>>", update_categories)

category_dropdown = ttk.Combobox(root, textvariable=category_var, state="readonly")
category_dropdown.grid(row=1, column=1, padx=5, pady=5)
update_categories()

# Entry fields
tk.Entry(root, textvariable=amount_var).grid(row=2, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Add Transaction", command=add_transaction, bg="green", fg="white").grid(row=3, column=0, pady=10)
tk.Button(root, text="Delete Transaction", command=delete_transaction, bg="red", fg="white").grid(row=3, column=1, pady=10)
tk.Button(root, text="Show Graph", command=show_graph, bg="purple", fg="white").grid(row=4, column=0, pady=5)
tk.Button(root, text="Exit", command=exit_app, bg="black", fg="white").grid(row=4, column=1, pady=5)

# Summary Section
summary_frame = tk.Frame(root, bd=2, relief="solid", padx=10, pady=10)
summary_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

tk.Label(summary_frame, text="Summary", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)

income_label = tk.Label(summary_frame, text="Total Income: 0.00", font=("Arial", 10, "bold"))
income_label.grid(row=1, column=0, columnspan=2, pady=5)

expense_label = tk.Label(summary_frame, text="Total Expense: 0.00", font=("Arial", 10, "bold"))
expense_label.grid(row=2, column=0, columnspan=2, pady=5)

investment_label = tk.Label(summary_frame, text="Total Investment: 0.00", font=("Arial", 10, "bold"))
investment_label.grid(row=3, column=0, columnspan=2, pady=5)

savings_label = tk.Label(summary_frame, text="Savings: 0.00", font=("Arial", 12, "bold"), fg="blue")
savings_label.grid(row=4, column=0, columnspan=2, pady=5)

# Budget Input & Status
tk.Label(summary_frame, text="Budget ():").grid(row=5, column=0)
tk.Entry(summary_frame, textvariable=budget_var).grid(row=5, column=1)
budget_status_label = tk.Label(summary_frame, text="Set a budget!", fg="orange")
budget_status_label.grid(row=6, column=0, columnspan=2)

# Listbox for transactions
listbox = tk.Listbox(root, width=60, height=10)
listbox.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Load transactions
refresh_transactions()

# Run GUI
root.mainloop()
