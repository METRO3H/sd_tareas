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
    
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (table_name, idx))
            
            db_result = cursor.fetchone()[0]

            return db_result

def save_qa(table_name, idx, question, yahoo_answer, gemini_answer, score):
    
    query = "CALL save_qa(%s, %s, %s, %s, %s, %s)"
    
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (table_name, idx, question, yahoo_answer, gemini_answer, score))
            