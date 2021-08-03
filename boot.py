# Imports
from models.Product import *
from models.Money import Money
from models.Order import Order
from models.Customer import *
from services.TestData import TestDataService

# Initialization
tds = TestDataService()
prf = ProductRepositoryFactory()
crf = CustomerRepositoryFactory()
