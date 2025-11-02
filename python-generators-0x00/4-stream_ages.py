#!/usr/bin/python3
"""Memory-Efficient Aggregation with Generators"""

import seed


def stream_user_ages():
    """Generator that yields user ages one by one from the database"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row["age"]

    connection.close()


def average_user_age():
    """Calculate and print the average age using the generator"""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("Average age of users: 0")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    average_user_age()
