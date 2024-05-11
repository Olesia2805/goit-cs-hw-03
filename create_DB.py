import logging
from psycopg2 import DatabaseError

from connect_DB import connect


def create_table(conn, sql_stmt: str):
    cursor = conn.cursor()
    try:
        cursor.execute(sql_stmt)
        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        cursor.close()


def create_tables():
    users_stmt = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
    """

    status_stmt = """
    CREATE TABLE status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );
    """

    tasks_stmt = """
    CREATE TABLE tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        status_id INTEGER,
        user_id INTEGER,
        FOREIGN KEY (status_id) REFERENCES status(id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """

    try:
        with connect() as conn:
            create_table(conn, users_stmt)
            create_table(conn, status_stmt)
            create_table(conn, tasks_stmt)
    except RuntimeError as e:
        logging.error(e)