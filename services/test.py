import requests
import json


class TestDataService:
    def create_test_products(self, quantity=10):
        url = f'https://fakestoreapi.com/products?limit={quantity}'
        res = requests.get(url)
        if res.status_code == 200:
            data = json.loads(res.text)
            self.products = data
            return data
        else: raise SystemExit(f'Unable to connect: connection error {res.status_code}')

    def __str__(self): return '\nNothing here\n' if self.products == None else f'\nProducts: {self.products}\n'
