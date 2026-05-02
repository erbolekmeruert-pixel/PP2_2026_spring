import os


DB_CONFIG = {
    "dbname": os.getenv("SNAKE_DB", "snake_game"),
    "user": os.getenv("SNAKE_USER", "postgres"),
    "password": os.getenv("SNAKE_PASSWORD", "postgres"),
    "host": os.getenv("SNAKE_HOST", "localhost"),
    "port": int(os.getenv("SNAKE_PORT", "5432")),
}