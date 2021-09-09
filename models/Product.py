class Product:
    def __init__(self, id_, name, price, categoryId):
        self.id = id_
        self.inDB = False
        self.name = name
        self.price = price
        self.categoryId = categoryId

    def __str__(self):
        title = f"--- Product \"{self.name}\" ---"
        id_ = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        price = f'Price: {self.price}'
        categoryId = f'Category id: {self.categoryId}'
        return f'\n\n{title}\n{id_}\n{inDB}\n{price}\n{categoryId}\n\n'

    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.name, self.price, self.categoryId]}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) == int:
                    object.__setattr__(self, name, value)
                else:
                    raise TypeError('id must have an int value')
        elif name == 'inDB':
            if value in (True, False):
                object.__setattr__(self, name, value)
            else:
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
                object.__setattr__(self, name, value)
        elif name == 'price':
            from .Money import Money
            # check type
            if type(value) != Money:
                raise TypeError('price must be Money type')
            else:
                object.__setattr__(self, name, value)
        elif name == 'categoryId':
            if type(value) != int:
                raise TypeError('categoryId must be int type')
            else:
                object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def __eq__(self, other):
        if type(other) == Product:
            if self.id == other.id:
                return True
            else:
                return False


class ProductRepositoryFactory:
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        products = self.pgds.query('SELECT p.id, p.name,\
            p.price_id, p.category_id FROM products AS p')
        if len(products) != 0:
            from .Money import MoneyRepositoryFactory
            mrf = MoneyRepositoryFactory(self.pgds)
            prods = []
            for row in products:
                money = mrf.findById(row[2])
                p = self.getProduct(row[0], row[1], money, row[3])
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
    def getProduct(self, id_, name, price, categoryId):
        return Product(id_, name, price, categoryId)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query('SELECT * FROM products')
        if len(res) > 0:
            from .Money import MoneyRepositoryFactory
            mrf = MoneyRepositoryFactory(self.pgds)
            products = []
            for row in res:
                money = mrf.findById(row[2])
                p = self.getProduct(row[0], row[1], money, row[3])
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
                VALUES (\'{product.name}\', now(), {product.price.id}, {product.categoryId})\
                RETURNING id')[0][0]
            product.inDB = True
        elif product.inDB:
            self.pgds.query(f'''
                UPDATE products
                SET name = \'{product.name}\',
                    updated = now(),
                    price_id = {product.price.id},
                    category_id = {product.categoryId}
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
                    VALUES (\'{product.name}\', now(), {product.price.id}, {product.categoryId})\
                    RETURNING id')[0][0]
                product.inDB = True
            elif product.inDB:
                self.pgds.query(f'''
                    UPDATE products
                    SET name = \'{product.name}\',
                        updated = now(),
                        price_id = {product.price.id},
                        category_id = {product.categoryId}
                    WHERE id = {product.id}
                ''')

    def findById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Search
        res = self.pgds.query(f'''
            SELECT id, name, price_id, category_id FROM products
            WHERE id = {id_}
        ''')
        if len(res) != 0:
            from .Money import MoneyRepositoryFactory
            mrf = MoneyRepositoryFactory()
            data = res[0]
            money = mrf.findById(data[2])
            p = self.getProduct(data[0], data[1], money, data[3])
            p.inDB = True
            return p

    def deleteById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Delete object data
        self.pgds.query(f'DELETE FROM products WHERE id = {id_}')
