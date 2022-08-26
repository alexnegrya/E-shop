# Setup logging
import logging
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] (%(name)s) - %(message)s',
    datefmt='%H:%M:%S',
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)


# Imports
from models import *
from services.test import TestDataService
from services.pg import PostgresDataService
import os
from psycopg2.errors import UndefinedTable

logger.info('All modules and libraries imported')


# Services initialization
tds = TestDataService()
PASSWORD = os.environ.get('ESHOP_DB_PASSWORD')
if PASSWORD != None:
    pgds = PostgresDataService('localhost', 'eshop', 'eshop_admin', PASSWORD)
    pgds.open()

    logger.info('Database service initialized')
else:
    raise SystemExit('ESHOP_DB_PASSWORD system variable was not found, have you followed all instructions in project page on GitHub?')


# Creating missing tables
TABLES = (
    'addresses', 'categories', 'clients', 'contacts', 'money',
    'payments', 'products', 'ratings', 'services', 'shops',
    'stock_items', 'orders', 'orders_items'
)
created_tables = []
for table in TABLES:
    try:
        pgds.query(f'SELECT * FROM {table} LIMIT 1')
    except UndefinedTable:
        pgds.conn.rollback()
        with open(f'sql/tables/{table}.sql') as file:
            pgds.query(file.read())
        created_tables.append(table)
logger.info(f'The following missing database tables created: {", ".join(created_tables)}' if len(created_tables) > 0 else 'All database tables exist')

# Inserting test data if all tables were created now and user agrees
# if len(created_tables) == len(TABLES):
#     while True:
#         os.system('clear')
#         choice = input('\nNew database found, auto insert test data? (y/n) >>> ').lower()
#         if choice.startswith('y'):
#             with open('sql/scripts/insert.sql') as file: pgds.query(file.read())
#         elif choice.startswith('n'): break


# Repositories initialization
pm = ProductsManager(pgds)
cm = ClientsManager(pgds)
am = AddressesManager(pgds)
conm = ContactsManager(pgds)
catsm = CategoriesManager(pgds)

logger.info('Models factories intialized')
