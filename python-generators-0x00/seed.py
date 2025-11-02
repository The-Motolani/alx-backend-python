#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

# ------------------------------
# Connect to MySQL server (root connection)
# ------------------------------
def connect_db():
    """Connect to MySQL server."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"  # Replace with your MySQL root password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# ------------------------------
# Create database if not exists
# ------------------------------
def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        cursor.close()

# ------------------------------
# Connect to ALX_prodev database
# ------------------------------
def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # Replace with your MySQL root password
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

# ------------------------------
# Create table user_data
# ------------------------------
def create_table(connection):
    """Create user_data table if it does not exist."""
    cursor = connection.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX (user_id)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

# ------------------------------
# Insert data from CSV file
# ------------------------------
def insert_data(connection, csv_file):
    """Insert data into user_data table from CSV."""
    cursor = connection.cursor()
    try:
        with open(csv_file, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Generate UUID for user_id if not in CSV
                user_id = str(uuid.uuid4())
                name = row.get("name")
                email = row.get("email")
                age = row.get("age")

                # Insert only if email does not exist (avoid duplicates)
                cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))
        connection.commit()
        print("Data inserted successfully")
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()
