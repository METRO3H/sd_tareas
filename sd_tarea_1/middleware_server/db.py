import os
import psycopg

connection_parameters = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "dbname": os.getenv("POSTGRES_DB")
}

def get_connection():
    connection = psycopg.connect(**connection_parameters)
    return connection


def check_qa(table_name, idx):
    query = "SELECT check_qa(%s, %s)"
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (table_name, idx))
                db_result = cursor.fetchone()[0]

                return db_result
            
    except Exception as e:
        print("Error Postgres:", e)
        return False



def register_cache_event(table_name, idx, event_type):

    if event_type not in ('hit', 'miss'):
        raise ValueError("event_type must be 'hit' or 'miss'")

    query = "CALL register_cache_event(%s, %s, %s)"
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (table_name, idx, event_type))
        return True
    except Exception as e:
        print("Error registering cache event:", e)
        return False

def save_qa(table_name, idx, question, yahoo_answer, gemini_answer, score):
    query = "CALL save_qa(%s, %s, %s, %s, %s, %s)"
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (table_name, idx, question, yahoo_answer, gemini_answer, score))
        print(f"QA with idx {idx} saved in table {table_name} successfully")
        return True
    except Exception as e:
        print("Error saving QA in table ", table_name, ":")
        print(e)
        return False
            