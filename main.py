import csv
import os
from collections import defaultdict
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"

def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])

def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category (Food/Travel/Bills/Shopping/Others): ")
    amount = input("Enter amount: ")
    description = input("Enter description: ")

    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

    print("Expense added successfully!")
def view_expenses():
    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        if len(rows) <= 1:
            print("\nNo expenses found.")
            return

        print("\n--- All Expenses ---")
        print("-" * 60)
        print(f"{'Date':<12} | {'Category':<12} | {'Amount':<10} | Description")
        print("-" * 60)

        for row in rows[1:]:
            print(f"{row[0]:<12} | {row[1]:<12} | {row[2]:<10} | {row[3]}")

        print("-" * 60)
def monthly_summary():
    month = input("Enter month (YYYY-MM): ")
    total = 0

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Date"].startswith(month):
                total += float(row["Amount"])

    print(f"\nTotal expenses for {month}: ₹{total:.2f}")
def category_breakdown():
    month = input("Enter month (YYYY-MM): ")
    categories = defaultdict(float)

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Date"].startswith(month):
                categories[row["Category"]] += float(row["Amount"])

    if not categories:
        print("\nNo expenses found for this month.")
        return

    print(f"\n--- Category Breakdown for {month} ---")
    print("-" * 40)

    for category, amount in categories.items():
        print(f"{category:<15}: ₹{amount:.2f}")

    print("-" * 40)
def highest_spending_category():
    month = input("Enter month (YYYY-MM): ")
    categories = defaultdict(float)

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Date"].startswith(month):
                categories[row["Category"]] += float(row["Amount"])

    if not categories:
        print("\nNo expenses found for this month.")
        return

    highest_category = max(categories, key=categories.get)
    highest_amount = categories[highest_category]

    print(f"\nHighest spending category in {month}: {highest_category} (₹{highest_amount:.2f})")
def generate_pie_chart():
    month = input("Enter month (YYYY-MM): ")
    categories = defaultdict(float)

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Date"].startswith(month):
                categories[row["Category"]] += float(row["Amount"])

    if not categories:
        print("\nNo expenses found for this month.")
        return

    labels = list(categories.keys())
    amounts = list(categories.values())

    plt.figure(figsize=(8, 8))
    plt.pie(amounts, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(f"Expense Distribution for {month}")
    plt.axis('equal')
    plt.show()
def smart_insights():
    month = input("Enter month (YYYY-MM): ")
    categories = defaultdict(float)

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Date"].startswith(month):
                categories[row["Category"]] += float(row["Amount"])

    if not categories:
        print("\nNo expenses found for this month.")
        return

    highest_category = max(categories, key=categories.get)
    highest_amount = categories[highest_category]

    print(f"\n--- Smart Insight for {month} ---")
    print(f"You are spending the most on: {highest_category} (₹{highest_amount:.2f})")

    if highest_category.lower() == "food":
        print("Suggestion: Try reducing outside meals or ordering less frequently.")
    elif highest_category.lower() == "travel":
        print("Suggestion: Consider using public transport or planning trips efficiently.")
    elif highest_category.lower() == "bills":
        print("Suggestion: Review utility usage and reduce unnecessary electricity/water consumption.")
    elif highest_category.lower() == "shopping":
        print("Suggestion: Avoid impulse purchases and plan your shopping budget.")
    else:
        print("Suggestion: Monitor this category closely and try setting a monthly limit.")
def main():
    initialize_file()

    while True:
        print("\n=== Smart Expense Tracker ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Summary")
        print("4. Category Breakdown")
        print("5. Highest Spending Category")
        print("6. Generate Pie Chart")
        print("7. Smart Insights")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            monthly_summary()
        elif choice == '4':
            category_breakdown()
        elif choice == '5':
            highest_spending_category()
        elif choice == '6':
            generate_pie_chart()
        elif choice == '7':
            smart_insights()
        elif choice == '8':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
