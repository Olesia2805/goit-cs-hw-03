import create_DB
from seed import seed

if __name__ == '__main__':
    create_DB.create_tables()
    seed()