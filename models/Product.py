from db.templates import *


class Product(Model):
    def __init__(self, id_, name, price, category_id):
        self.id = id_
        self.inDB = False
        self.name = name
        self.price = price
        self.category_id = category_id

    def __str__(self):
        title = f"--- Product \"{self.name}\" ---"
        id_ = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        price = f'Price: {self.price}'
        category_id = f'Category id: {self.category_id}'
        return f'\n\n{title}\n{id_}\n{inDB}\n{price}\n{category_id}\n\n'

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.name, self.price, self.category_id]}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) != int:
                    raise TypeError('id must have an int value')
        elif name == 'inDB':
            if value not in (True, False):
                raise TypeError('value for inDB attribute must be True or False only')
        elif name == 'name':
            if type(value) != str:
                raise TypeError('name must be a string')
            elif value == '':
                raise NameError('name cannot be an empty string')
            else:
                # Spliting name by letters
                splited = []
                for i in range(len(value)):
                    splited.append(value[i])
                # Checking name for letters repition
                repeated_numbers = {}
                for i in range(len(splited)):
                    if splited[i] not in repeated_numbers:
                        repeated_numbers[splited[i]] = 1
                    else:
                        repeated_numbers[splited[i]] += 1
                # Checking name for the same letters only
                for i in range(len(repeated_numbers)):
                    if repeated_numbers[splited[i]] == len(value):
                        raise NameError(
                            'the name contains only the same letters')
        elif name == 'price':
            from .Money import Money
            if type(value) != Money: raise TypeError('price must be Money type')
        elif name == 'category_id':
            if type(value) != int: raise TypeError('category_id must be int type')
        object.__setattr__(self, name, value)

    def __eq__(self, other): return self.id == other.id if type(other) == Product else False


class ProductRepositoryFactory(ModelRepositoryFactory):
    def __init__(self, pgds):
        self.pgds = pgds

        from .Money import MoneyRepositoryFactory
        self.mrf = MoneyRepositoryFactory(self.pgds)

    def __str__(self):
        products = self.pgds.query('SELECT p.id, p.name,\
            p.price_id, p.category_id FROM products AS p')
        if len(products) != 0:
            prods = []
            for row in products:
                money = self.mrf.find_by_id(row[2])
                p = self.get_product(row[0], row[1], money, row[3])
                p.inDB = True
                prods.append(p)
            out = ''
            for product in prods:
                out = out + str(product)
        else:
            out = '\nNo products here\n'
        return out

    def __repr__(self):
        return str(self.pgds.query('SELECT * FROM products'))

    # ##### Factory methods #####
    def get_product(self, id_, name, price, category_id):
        return Product(id_, name, price, category_id)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query('SELECT * FROM products')
        if len(res) > 0:
            products = []
            for row in res:
                money = self.mrf.find_by_id(row[2])
                p = self.get_product(row[0], row[1], money, row[3])
                p.inDB = True
                products.append(p)
            return products
        else:
            return []

    def save(self, product):
        # Type verify
        if type(product) != Product:
            raise TypeError('the entity should be Product type')
        # Save object data
        if product.inDB == False:
            product.id = self.pgds.query(f'INSERT INTO products(name, created, price_id, category_id)\
                VALUES (\'{product.name}\', now(), {product.price.id}, {product.category_id})\
                RETURNING id')[0][0]
            product.inDB = True
        elif product.inDB:
            self.pgds.query(f'''
                UPDATE products
                SET name = \'{product.name}\',
                    updated = now(),
                    price_id = {product.price.id},
                    category_id = {product.category_id}
                WHERE id = {product.id}
            ''')

    def save_many(self, *products):
        # Checking object quantity
        l = len(products)
        if l in [0, 1]:
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(len(products)):
            if type(products[i]) != Product:
                raise TypeError(f'object number {i+1} is not a Product type')
        # Save objects data
        for product in products:
            if product.inDB == False:
                product.id = self.pgds.query(f'INSERT INTO products(name, created, price_id, category_id)\
                    VALUES (\'{product.name}\', now(), {product.price.id}, {product.category_id})\
                    RETURNING id')[0][0]
                product.inDB = True
            elif product.inDB:
                self.pgds.query(f'''
                    UPDATE products
                    SET name = \'{product.name}\',
                        updated = now(),
                        price_id = {product.price.id},
                        category_id = {product.category_id}
                    WHERE id = {product.id}
                ''')

    def find_by_id(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Search
        res = self.pgds.query(f'''
            SELECT id, name, price_id, category_id FROM products
            WHERE id = {id_}
        ''')
        if len(res) != 0:
            data = res[0]
            money = self.mrf.find_by_id(data[2])
            p = self.get_product(data[0], data[1], money, data[3])
            p.inDB = True
            return p

    def delete_by_id(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Delete object data
        self.pgds.query(f'DELETE FROM products WHERE id = {id_}')
