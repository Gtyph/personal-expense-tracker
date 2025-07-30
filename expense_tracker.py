import sqlite3
from datetime import datetime

# Connect to SQLite DB
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL,
        note TEXT
    )
""")
conn.commit()

def add_expense():
    date = input("Date (YYYY-MM-DD) [Leave empty for today]: ") or datetime.today().strftime('%Y-%m-%d')
    category = input("Category (e.g. Food, Transport, etc): ")
    amount = float(input("Amount (€): "))
    note = input("Note (optional): ")
    cursor.execute("INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)", (date, category, amount, note))
    conn.commit()
    print("✅ Expense added!")

def view_expenses():
    cursor.execute("SELECT date, category, amount, note FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    print("\n📄 All Expenses:")
    for row in rows:
        print(f"{row[0]} | {row[1]} | €{row[2]:.2f} | {row[3]}")

def show_summary():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0
    print(f"\n💰 Total spent: €{total:.2f}")

def menu():
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Summary")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option.")

menu()
conn.close()

