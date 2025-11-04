#!/usr/bin/env python3
import time
import sqlite3
import functools

# Global cache dictionary
query_cache = {}


def with_db_connection(func):
    """Decorator to open and close a database connection automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def cache_query(func):
    """Decorator to cache query results based on the SQL query string"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query string from arguments
        query = kwargs.get('query') if 'query' in kwargs else args[1] if len(args) > 1 else None

        # Check if query result is already cached
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]

        # Otherwise, execute the function and store the result
        print(f"Caching result for new query: {query}")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call will cache the result
if __name__ == "__main__":
    users = fetch_users_with_cache(query="SELECT * FROM users")

    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
