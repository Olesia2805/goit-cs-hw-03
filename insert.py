import logging
from psycopg2 import DatabaseError
from faker import Faker
import random

fake = Faker('uk_UA')
COUNT = 100


def status(conn, status_names):
    cursor = conn.cursor()
    try:
        for name in status_names:
            cursor.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING;", (name,))

        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        cursor.close()

def users(conn, sql_stmt: str):
    cursor = conn.cursor()
    try:
        for _ in range(COUNT):
            fullname = fake.name()
            email = fake.email()
            cursor.execute(sql_stmt, (fullname, email))
        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        cursor.close()

def tasks(conn, sql_stmt: str):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM status;")
        status_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT id FROM users;")
        user_ids = [row[0] for row in cursor.fetchall()]

        for _ in range(COUNT):
            title = fake.sentence(nb_words=6)
            description = fake.text()
            status_id = random.choice(status_ids)
            user_id = random.choice(user_ids)
            cursor.execute(sql_stmt, (title, description, status_id, user_id))
        conn.commit()

    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        cursor.close()