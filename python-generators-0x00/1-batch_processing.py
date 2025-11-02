import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that fetches rows from user_data table in batches."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch  # use yield, not return

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Processes each batch to filter and print users older than 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                yield user  # use yield here too, no print or return
