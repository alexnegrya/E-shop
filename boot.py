# Imports
from models.Product import *
from models.Money import Money
from models.Order import Order
from models.Customer import *
from models.Address import *
from services.TestData import TestDataService
from services.PGDataService import PGDataService

# Services initialization
tds = TestDataService()
with open('sql/user_password.txt', 'r') as file:
    password = file.read()
pgds = PGDataService('localhost', 'eshop', 'postgres', password)
pgds.open()

# Repositories initialization
prf = ProductRepositoryFactory(pgds)
crf = CustomerRepositoryFactory(pgds)
