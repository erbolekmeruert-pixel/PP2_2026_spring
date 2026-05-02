import csv
from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name TEXT,
            phone TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_from_csv():
    conn = get_connection()
    cur = conn.cursor()
    with open("contacts.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  
        for row in reader:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()
    conn.close()

def insert_from_console():
    conn = get_connection()
    cur = conn.cursor()
    name = input("Name: ")
    phone = input("Phone: ")
    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    conn.close()

def show_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook")
    for row in cur.fetchall():
        print(row)
    conn.close()

def update_contact():
    conn = get_connection()
    cur = conn.cursor()
    name = input("Name to update: ")
    new_phone = input("New phone: ")
    cur.execute("UPDATE phonebook SET phone=%s WHERE name=%s", (new_phone, name))
    conn.commit()
    conn.close()

def delete_contact():
    conn = get_connection()
    cur = conn.cursor()
    keyword = input("Enter name or phone to delete: ")
    cur.execute("DELETE FROM phonebook WHERE name=%s OR phone=%s", (keyword, keyword))
    conn.commit()
    conn.close()



# additional
from phonebook import *

create_table()

while True:
    print("\n1 - Insert CSV")
    print("2 - Add from console")
    print("3 - Show contacts")
    print("4 - Update contact")
    print("5 - Delete contact")
    print("0 - Exit")
    choice = input("Choose: ")

    if choice == "1":
        insert_from_csv()
    elif choice == "2":
        insert_from_console()
    elif choice == "3":
        show_contacts()
    elif choice == "4":
        update_contact()
    elif choice == "5":
        delete_contact()
    elif choice == "0":
        break
    else:
        print("ERROR ENTER!")