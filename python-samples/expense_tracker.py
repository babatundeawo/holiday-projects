import csv
from datetime import datetime
import os

FILENAME = "expenses.csv"

def initialize_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Description", "Amount"])

def add_expense():
    date = datetime.now().strftime("%Y-%m-%d")
    category = input("Enter category (e.g., Food, Transport, Bills): ").capitalize()
    description = input("Enter short description: ")
    amount = float(input("Enter amount spent: ₦"))

    with open(FILENAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, description, amount])
    print("Expense recorded successfully!\n")

def view_expenses():
    with open(FILENAME, mode="r") as file:
        reader = csv.reader(file)
        next(reader)
        print(f"\n{'Date':<12} {'Category':<12} {'Description':<20} {'Amount (₦)':>10}")
        print("-" * 60)
        for row in reader:
            print(f"{row[0]:<12} {row[1]:<12} {row[2]:<20} {row[3]:>10}")
        print()

def summarize_by_category():
    totals = {}
    with open(FILENAME, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            category = row["Category"]
            amount = float(row["Amount"])
            totals[category] = totals.get(category, 0) + amount

    print("\nExpense Summary by Category:")
    print("-" * 35)
    for category, total in totals.items():
        print(f"{category:<15} ₦{total:.2f}")
    print()

def main():
    initialize_file()
    while True:
        print("Expense Tracker Menu")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Summary by Category")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            summarize_by_category()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.\n")

if __name__ == "__main__":
    main()
