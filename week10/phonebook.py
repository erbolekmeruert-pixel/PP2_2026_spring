from connect import connect


def insert_or_update(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()


def search(pattern):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def paginate(limit, offset):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def delete_contact(value):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()

    cur.close()
    conn.close()


# 🔥 Меню
if __name__ == "__main__":
    while True:
        print("\n1 - Insert/Update")
        print("2 - Search")
        print("3 - Pagination")
        print("4 - Delete")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            insert_or_update(name, phone)

        elif choice == "2":
            pattern = input("Search: ")
            search(pattern)

        elif choice == "3":
            limit = int(input("Limit: "))
            offset = int(input("Offset: "))
            paginate(limit, offset)

        elif choice == "4":
            value = input("Name or phone: ")
            delete_contact(value)

        elif choice == "0":
            break

        else:
            print("ERROR")