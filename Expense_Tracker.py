import csv
from pathlib import Path

FILE = Path("expenses.csv")

def add_expense():
    amount = input("Amount: ")
    category = input("Category: ")
    with FILE.open("a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([amount, category])

def summary():
    totals = {}
    if not FILE.exists():
        print("No expenses recorded.")
        return

    with FILE.open() as f:
        reader = csv.reader(f)
        for amount, category in reader:
            totals[category] = totals.get(category, 0) + float(amount)

    for cat, total in totals.items():
        print(f"{cat}: £{total:.2f}")

def menu():
    while True:
        print("\n1) Add expense\n2) View summary\n3) Exit")
        choice = input("Choose: ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            summary()
        elif choice == "3":
            break

if __name__ == "__main__":
    menu()