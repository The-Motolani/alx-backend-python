#!/usr/bin/env python3
import sqlite3


class ExecuteQuery:
    """Custom context manager to execute a database query with parameters"""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Open connection, execute the query, and return the result"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        # Fetch all results immediately
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """Close cursor and connection automatically"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # Return False so that exceptions (if any) are not suppressed
        return False


# Using the context manager
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        print(results)
