from datetime import datetime
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
database_name = os.getenv("DATABASE_NAME")

db = sqlite3.connect(database_name)
cursor = db.cursor()

def create_orders_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    print("✅ Orders table ready")
    db.commit()


def create_items_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
        """
    )

    print("✅ Items table ready")
    db.commit()


def start_db():
    create_orders_table()
    create_items_table()

    db.close()


async def get_db():
    db = sqlite3.connect(str(database_name))
    db.row_factory = sqlite3.Row

    return db
