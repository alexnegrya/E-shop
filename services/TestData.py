class TestDataService:
    def __init__(self):
        self.products = None

    def getTestProducts(self, quantity=10):
        import requests
        import json
        url = f'https://fakestoreapi.com/products?limit={quantity}'
        res = requests.get(url)
        if res.status_code == 200:
            data = json.loads(res.text)
            self.products = data
            return data
        else:
            raise SystemExit(f'Unable to connect: connection error {res.status_code}')

    def __str__(self):
        if self.products == None:
            return '\nNothing here\n'
        else:
            return f'\nProducts: {self.products}\n'
