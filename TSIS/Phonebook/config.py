import os


DB_CONFIG = {
    "dbname": os.getenv("PHONEBOOK_DB", "phonebook"),
    "user": os.getenv("PHONEBOOK_USER", "postgres"),
    "password": os.getenv("12345678", "postgres"),
    "host": os.getenv("PHONEBOOK_HOST", "localhost"),
    "port": int(os.getenv("PHONEBOOK_PORT", "5432")),
}