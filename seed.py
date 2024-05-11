import logging

import connect_DB
import insert


def seed():
    logging.basicConfig(level=logging.INFO)

    status_names = ['new', 'in progress', 'completed']

    insert_users_stmt = """
    INSERT INTO users (fullname, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING;
    """

    insert_tasks_stmt = """
    INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);
    """

    try:
        with connect_DB.connect() as conn:
            insert.status(conn, status_names)
            insert.users(conn, insert_users_stmt)
            insert.tasks(conn, insert_tasks_stmt)
    except RuntimeError as e:
        logging.error(e)