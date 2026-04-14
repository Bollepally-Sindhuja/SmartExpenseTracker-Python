import csv
import os
from collections import defaultdict
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"

# ----------------------------
# Initialize CSV File
# ----------------------------
def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])

# ----------------------------
# Add Expense
# ----------------------------
def add_expense():
    date = date_entry.get().strip()
    category = category_combo.get().strip()
    amount = amount_entry.get().strip()
    description = description_entry.get().strip()

    if not date or not category or not amount or not description:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a valid number.")
        return

    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

    messagebox.showinfo("Success", "Expense added successfully!")

    date_entry.delete(0, tk.END)
    category_combo.set("")
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

# ----------------------------
# View Expenses
# ----------------------------
def view_expenses():
    expense_window = tk.Toplevel(root)
    expense_window.title("All Expenses")
    expense_window.geometry("800x400")
    expense_window.config(bg="#f4f6f8")

    title = tk.Label(expense_window, text="All Expenses", font=("Arial", 16, "bold"), bg="#f4f6f8")
    title.pack(pady=10)

    tree = ttk.Treeview(expense_window, columns=("Date", "Category", "Amount", "Description"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount (₹)")
    tree.heading("Description", text="Description")

    tree.column("Date", width=120, anchor="center")
    tree.column("Category", width=120, anchor="center")
    tree.column("Amount", width=120, anchor="center")
    tree.column("Description", width=350, anchor="center")

    tree.pack(fill="both", expand=True, padx=20, pady=10)

    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            tree.insert("", tk.END, values=row)

# ----------------------------
# Get Monthly Category Totals
# ----------------------------
def get_monthly_categories(month):
    categories = defaultdict(float)

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Date"].startswith(month):
                categories[row["Category"]] += float(row["Amount"])

    return categories

# ----------------------------
# Monthly Summary
# ----------------------------
def monthly_summary():
    month = month_entry.get().strip()

    if not month:
        messagebox.showerror("Error", "Please enter month in YYYY-MM format.")
        return

    total = 0
    found = False

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Date"].startswith(month):
                total += float(row["Amount"])
                found = True

    if not found:
        messagebox.showerror("No Data", f"No expenses found for {month}.")
        return

    messagebox.showinfo("Monthly Summary", f"Total expenses for {month}: ₹{total:.2f}")

# ----------------------------
# Category Breakdown
# ----------------------------
def category_breakdown():
    month = month_entry.get().strip()
    categories = get_monthly_categories(month)

    if not month:
        messagebox.showerror("Error", "Please enter month in YYYY-MM format.")
        return

    if not categories:
        messagebox.showerror("Error", "No expenses found for this month.")
        return

    breakdown_window = tk.Toplevel(root)
    breakdown_window.title(f"Category Breakdown - {month}")
    breakdown_window.geometry("450x350")
    breakdown_window.config(bg="#f4f6f8")

    title_label = tk.Label(
        breakdown_window,
        text=f"Category Breakdown - {month}",
        font=("Arial", 16, "bold"),
        bg="#f4f6f8"
    )
    title_label.pack(pady=10)

    tree = ttk.Treeview(breakdown_window, columns=("Category", "Amount"), show="headings")
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount (₹)")
    tree.column("Category", width=180, anchor="center")
    tree.column("Amount", width=180, anchor="center")
    tree.pack(fill="both", expand=True, padx=20, pady=20)

    for category, amount in categories.items():
        tree.insert("", tk.END, values=(category, f"{amount:.2f}"))

# ----------------------------
# Highest Spending Category
# ----------------------------
def highest_spending_category():
    month = month_entry.get().strip()
    categories = get_monthly_categories(month)

    if not month:
        messagebox.showerror("Error", "Please enter month in YYYY-MM format.")
        return

    if not categories:
        messagebox.showerror("Error", "No expenses found for this month.")
        return

    highest_category = max(categories, key=categories.get)
    highest_amount = categories[highest_category]

    messagebox.showinfo(
        "Highest Spending Category",
        f"Highest spending category in {month}:\n\n{highest_category} (₹{highest_amount:.2f})"
    )

# ----------------------------
# Pie Chart
# ----------------------------
def generate_pie_chart():
    month = month_entry.get().strip()
    categories = get_monthly_categories(month)

    if not month:
        messagebox.showerror("Error", "Please enter month in YYYY-MM format.")
        return

    if not categories:
        messagebox.showerror("Error", "No expenses found for this month.")
        return

    labels = list(categories.keys())
    amounts = list(categories.values())

    plt.figure(figsize=(8, 8))
    plt.pie(amounts, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(f"Expense Distribution for {month}")
    plt.axis('equal')
    plt.show()

# ----------------------------
# Smart Insights
# ----------------------------
def smart_insights():
    month = month_entry.get().strip()
    categories = get_monthly_categories(month)

    if not month:
        messagebox.showerror("Error", "Please enter month in YYYY-MM format.")
        return

    if not categories:
        messagebox.showerror("Error", "No expenses found for this month.")
        return

    highest_category = max(categories, key=categories.get)
    highest_amount = categories[highest_category]

    insight = f"You are spending the most on: {highest_category} (₹{highest_amount:.2f})\n\n"

    if highest_category.lower() == "food":
        insight += "Suggestion: Try reducing outside meals or ordering less frequently."
    elif highest_category.lower() == "travel":
        insight += "Suggestion: Consider using public transport or planning trips efficiently."
    elif highest_category.lower() == "bills":
        insight += "Suggestion: Review utility usage and reduce unnecessary electricity/water consumption."
    elif highest_category.lower() == "shopping":
        insight += "Suggestion: Avoid impulse purchases and plan your shopping budget."
    else:
        insight += "Suggestion: Monitor this category closely and try setting a monthly limit."

    messagebox.showinfo("Smart Insights", insight)

# ----------------------------
# Monthly Expense Report
# ----------------------------
def monthly_expense_report():
    month = month_entry.get().strip()

    if not month:
        messagebox.showerror("Error", "Please enter month in YYYY-MM format.")
        return

    categories = get_monthly_categories(month)

    if not categories:
        messagebox.showerror("Error", f"No expenses found for {month}.")
        return

    total_expense = sum(categories.values())
    highest_category = max(categories, key=categories.get)
    highest_amount = categories[highest_category]

    if highest_category.lower() == "food":
        suggestion = "Try reducing outside meals or ordering less frequently."
    elif highest_category.lower() == "travel":
        suggestion = "Consider using public transport or planning trips efficiently."
    elif highest_category.lower() == "bills":
        suggestion = "Review utility usage and reduce unnecessary electricity/water consumption."
    elif highest_category.lower() == "shopping":
        suggestion = "Avoid impulse purchases and plan your shopping budget."
    else:
        suggestion = "Monitor this category closely and try setting a monthly limit."

    report_window = tk.Toplevel(root)
    report_window.title(f"Monthly Expense Report - {month}")
    report_window.geometry("550x550")
    report_window.config(bg="#f4f6f8")

    title_label = tk.Label(
        report_window,
        text=f"Monthly Expense Report - {month}",
        font=("Arial", 16, "bold"),
        bg="#f4f6f8"
    )
    title_label.pack(pady=10)

    total_label = tk.Label(
        report_window,
        text=f"Total Expense: ₹{total_expense:.2f}",
        font=("Arial", 13, "bold"),
        bg="#f4f6f8"
    )
    total_label.pack(pady=5)

    category_title = tk.Label(
        report_window,
        text="Category-wise Expenses",
        font=("Arial", 12, "bold"),
        bg="#f4f6f8"
    )
    category_title.pack(pady=10)

    tree = ttk.Treeview(report_window, columns=("Category", "Amount"), show="headings", height=6)
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount (₹)")
    tree.column("Category", width=180, anchor="center")
    tree.column("Amount", width=180, anchor="center")
    tree.pack(pady=10)

    for category, amount in categories.items():
        tree.insert("", tk.END, values=(category, f"{amount:.2f}"))

    highest_label = tk.Label(
        report_window,
        text=f"Highest Spending Category: {highest_category} (₹{highest_amount:.2f})",
        font=("Arial", 12, "bold"),
        bg="#f4f6f8"
    )
    highest_label.pack(pady=15)

    suggestion_title = tk.Label(
        report_window,
        text="Smart Suggestion",
        font=("Arial", 12, "bold"),
        bg="#f4f6f8"
    )
    suggestion_title.pack()

    suggestion_label = tk.Label(
        report_window,
        text=suggestion,
        wraplength=450,
        justify="center",
        font=("Arial", 11),
        bg="#f4f6f8"
    )
    suggestion_label.pack(pady=10)

# ----------------------------
# Initialize App
# ----------------------------
initialize_file()

root = tk.Tk()
root.title("Smart Expense Tracker")
root.geometry("700x760")
root.config(bg="#eaf2f8")
root.resizable(False, False)

# ----------------------------
# Title Section
# ----------------------------
title_label = tk.Label(
    root,
    text="Smart Expense Tracker",
    font=("Arial", 22, "bold"),
    bg="#eaf2f8",
    fg="#1f3b57"
)
title_label.pack(pady=15)

subtitle_label = tk.Label(
    root,
    text="Track, Analyze, and Understand Your Expenses",
    font=("Arial", 11),
    bg="#eaf2f8",
    fg="#4f6475"
)
subtitle_label.pack(pady=5)

# ----------------------------
# Input Frame
# ----------------------------
input_frame = tk.LabelFrame(root, text="Add New Expense", font=("Arial", 12, "bold"), padx=20, pady=15, bg="#ffffff")
input_frame.pack(padx=20, pady=15, fill="x")

tk.Label(input_frame, text="Date (YYYY-MM-DD):", bg="#ffffff", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=8)
date_entry = tk.Entry(input_frame, width=30)
date_entry.grid(row=0, column=1, pady=8, padx=10)

tk.Label(input_frame, text="Category:", bg="#ffffff", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=8)
category_combo = ttk.Combobox(input_frame, values=["Food", "Travel", "Bills", "Shopping", "Others"], width=27)
category_combo.grid(row=1, column=1, pady=8, padx=10)

tk.Label(input_frame, text="Amount:", bg="#ffffff", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=8)
amount_entry = tk.Entry(input_frame, width=30)
amount_entry.grid(row=2, column=1, pady=8, padx=10)

tk.Label(input_frame, text="Description:", bg="#ffffff", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=8)
description_entry = tk.Entry(input_frame, width=30)
description_entry.grid(row=3, column=1, pady=8, padx=10)

tk.Button(input_frame, text="Add Expense", width=20, command=add_expense).grid(row=4, column=0, columnspan=2, pady=15)

# ----------------------------
# Analysis Frame
# ----------------------------
analysis_frame = tk.LabelFrame(root, text="Monthly Analysis", font=("Arial", 12, "bold"), padx=20, pady=15, bg="#ffffff")
analysis_frame.pack(padx=20, pady=10, fill="x")

tk.Label(analysis_frame, text="Enter Month (YYYY-MM):", bg="#ffffff", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=8)
month_entry = tk.Entry(analysis_frame, width=30)
month_entry.grid(row=0, column=1, pady=8, padx=10)

# Buttons Grid
tk.Button(analysis_frame, text="View Expenses", width=22, command=view_expenses).grid(row=1, column=0, pady=8, padx=10)
tk.Button(analysis_frame, text="Monthly Summary", width=22, command=monthly_summary).grid(row=1, column=1, pady=8, padx=10)

tk.Button(analysis_frame, text="Category Breakdown", width=22, command=category_breakdown).grid(row=2, column=0, pady=8, padx=10)
tk.Button(analysis_frame, text="Highest Spending Category", width=22, command=highest_spending_category).grid(row=2, column=1, pady=8, padx=10)

tk.Button(analysis_frame, text="Generate Pie Chart", width=22, command=generate_pie_chart).grid(row=3, column=0, pady=8, padx=10)
tk.Button(analysis_frame, text="Smart Insights", width=22, command=smart_insights).grid(row=3, column=1, pady=8, padx=10)

tk.Button(analysis_frame, text="Monthly Expense Report", width=46, command=monthly_expense_report).grid(row=4, column=0, columnspan=2, pady=15)

# ----------------------------
# Run App
# ----------------------------
root.mainloop()