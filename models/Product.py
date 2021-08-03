class Product:
    __ids = []

    def __init__(self, name, price, categoryId):
        self.id = self.__get_id()
        self.name = name
        self.price = price
        self.categoryId = categoryId

    def __get_id(self):
        from random import randint
        ID = ''
        for v in range(randint(4, 6)):
            ID = ID + str(randint(0, 9))
        return int(ID)

    def __check_id(self, id_):
        if id_ not in self.__ids:
            if id_ < 1 or id_ > 1000000:
                raise ValueError(
                    'id must be greater then 0 and lesser then 1000000')
            elif type(id_) != int:
                raise TypeError('id must be an integer')
            else:
                return True
        else:
            return False

    def __str__(self):
        title = f"--- Product \"{self.name}\" ---"
        id = f"Id: {self.id}"
        price = f'Price: {self.price}'
        categoryId = f'Category id: {self.categoryId}'
        return f'\n\n{title}\n{id}\n{price}\n{categoryId}\n\n'

    def __repr__(self):
        return str(self)

    def __setattr__(self, name, value):
        if name == 'id':
            if self.__check_id(value):
                object.__setattr__(self, name, value)
            else:
                while True:
                    if value == self.id:
                        if self.__check_id(value):
                            self.id = self.__get_id()
                    else:
                        break
                object.__setattr__(self, name, value)
        elif name == '__ids':
            raise AttributeError('changing this attribute is not allowed')
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

    def __getattr__(self, name):
        if name == 'id':
            object.__getattribute__(self, str(name))
        elif name == '__ids':
            return tuple(self.__ids)

    def __eq__(self, other):
        if type(other) == Product:
            if self.id == other.id:
                return True
            else:
                return False


class ProductRepositoryFactory:
    def __init__(self):
        self._lastCreatedId = 0
        self._products = []

    def __str__(self):
        if len(self._products) != 0:
            out = ''
            for product in self._products:
                out = out + str(product)
        else:
            out = '\nThere are no products here\n'
        return out

    def __repr__(self):
        return str(self)

    # ##### Factory methods #####
    def getProduct(self, name, price, categoryId):
        obj = Product(name, price, categoryId)
        self._lastCreatedId += 1
        obj.id = self._lastCreatedId
        self._products.append(obj)
        return obj

    def get_last_id(self):
        return f"\n{'-'*10}\n" + 'Last created object id: ' + str(self._lastCreatedId) + f"\n{'-'*10}\n"

    # ##### Repository methods #####
    def all(self):
        return self._products.copy()

    def save(self, product):
        # Type verify
        if type(product) != Product:
            raise TypeError('the entity should only be Product type')
        # Id verify
        if len(self._products) != 0:
            for p in self._products:
                if product == p:
                    raise AttributeError(
                        'a Product object with this id already exists')
        self._products.append(product)

    def save_many(self, products_list):
        # checking products_list type
        if type(products_list) != list:
            raise TypeError('products you want save should be in the list')
        # checking object quantity
        if len(products_list) in [0, 1]:
            l = len(products_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(products_list)):
            if type(products_list[i]) != Product:
                raise TypeError(
                    f'object with index {i} is not a Product type')
        # checking objects id's
        for product in products_list:
            for p in self._products:
                if product == p:
                    raise AttributeError(
                        'a Product object with this id already exists')
        self._products.extend(products_list)

    def overwrite(self, products_list):
        # checking products_list type
        if type(products_list) != list:
            raise TypeError(
                'products you want overwrite should be in the list')
        # checking objects type
        for i in range(len(products_list)):
            if type(products_list[i]) != Product:
                raise TypeError(
                    f'object with index {i} is not a Product type')
        # checking objects id's
        for product in products_list:
            for p in self._products:
                if product == p:
                    raise AttributeError(
                        'a Product object with this id already exists')
        self._products = products_list

    def findById(self, id_, showMode=True):
        if type(id_) != int:
            raise TypeError('id must be int type')
        for product in self._products:
            if product.id == id_:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Product found by id [{id_}]:' + str(product) + f"\n{'-'*10}\n"
                else:
                    return product
        if showMode:
            return f"\n{'-'*10}\n" + f'Product found by id [{id_}]:' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return product

    def findByName(self, name, showMode=True):
        if type(name) != str:
            raise TypeError('name must be str type')
        # With a incomplete match with the name
        found = []
        for product in self._products:
            if name in product.name:
                found.append(product)
        if len(found) != 0:
            if showMode:
                out = ''
                for p in found:
                    out = out + str(p)
                return f"\n{'-'*10}\n" + f'Products found by name keyword \"{name}\":' + out + f"\n{'-'*10}\n"
            else:
                return found
        # With a complete match with the name
        for product in self._products:
            if product.name == name:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Found Product with name \"{name}\":' + str(product) + f"\n{'-'*10}\n"
                else:
                    return found
        if showMode:
            return f"\n{'-'*10}\n" + f'Found Product with name \"{name}\":' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return found
    
    def findByPrice(self, price, showMode=True):
        if type(price) != int:
            raise TypeError('price must be int type')
        # search
        found = []
        for product in self._products:
            if product.price == price:
                found.append(product)
        # output
        if showMode:
            if len(found) == 0:
                return f"\n{'-'*10}\n" + f'Products found by price [{price}]:' + f'\n\nNothing was found' + f"\n{'-'*10}\n"
            else:
                out = ''
                for product in found:
                    out = out + str(product)
                return f"\n{'-'*10}\n" + f'Products found by price [{price}]:' + out + f"\n{'-'*10}\n"
        else:
            return found
    
    def findByPrice(self, moneyId=None, amount=None, currencyId=None, showMode=True):
        # Check type
        args_names = ['moneyId', 'amount', 'currencyId']
        arg_pos = 0
        m = None
        a = None
        c = None
        for argument in (moneyId, amount, currencyId):
            if argument != None:
                if type(argument) != int:
                    raise TypeError(f'{args_names[arg_pos]} must be int type')
                if m == None:
                    m = True if arg_pos == 0 else False
                if a == None and arg_pos != 0:
                    a = True if arg_pos == 1 else False
                if c == None and arg_pos not in (0, 1):
                    c = True if arg_pos == 2 else False
            arg_pos += 1
        # Search
        # variants: [m], [a], [c], [m, c], [a, m], [a, c], [m, a, c]
        found = []
        if m and a and c:
            for product in self._products:
                if product.price.id == moneyId\
                    and product.price.amount == amount\
                        and product.price.currencyId == currencyId:
                    found.append(product)
            args = ''
            for arg in args_names:
                if arg == 'moneyId':
                    args = args + arg + f' - {moneyId}, '
                elif arg == 'amount':
                    args = args + arg + f' - {amount}, '
                else:
                    args = args + arg + f' - {currencyId}'
        elif a and m:
            for product in self._products:
                if product.price.amount == amount\
                        and product.price.id == moneyId:
                    found.append(product)
            args_names.pop(2)
            args_names.reverse()
            args = ''
            for arg in args_names:
                if arg == 'amount':
                    args = args + arg + f' - {amount}, '
                else:
                    args = args + arg + f' - {moneyId}'
        elif a and c:
            for product in self._products:
                if product.price.amount == amount\
                        and product.price.currencyId == currencyId:
                    found.append(product)
            args_names.pop(0)
            args = ''
            for arg in args_names:
                if arg == 'amount':
                    args = args + arg + f' - {amount}, '
                else:
                    args = args + arg + f' - {currencyId}'
        elif m and c:
            for product in self._products:
                if product.price.id == moneyId\
                        and product.price.currencyId == currencyId:
                    found.append(product)
            args_names.pop(1)
            args = ''
            for arg in args_names:
                if arg == 'moneyId':
                    args = args + arg + f' - {moneyId}, '
                else:
                    args = args + arg + f' - {currencyId}'
        elif m:
            for product in self._products:
                if product.price.id == moneyId:
                    found.append(product)
            args_names.pop(1)
            args_names.pop(1)
            args = args_names[0] + f' - {moneyId}'
        elif a:
            for product in self._products:
                if product.price.amount == amount:
                    found.append(product)
            args_names.pop(0)
            args_names.pop(1)
            args = args_names[0] + f' - {amount}'
        elif c:
            for product in self._products:
                if product.price.currencyId == currencyId:
                    found.append(product)
            args_names.pop(0)
            args_names.pop(0)
            args = args_names[0] + f' - {currencyId}'
        else:
            raise ValueError('at least one argument must be specified')
        # Output
        if len(found) != 0:
            if showMode:
                return f"\n{'-'*10}\n" + f'Products found by price {args}:' + f'\n{found}' + f"\n{'-'*10}\n"
            else:
                return found
        else:
            if showMode:
                return f"\n{'-'*10}\n" + f'Products found by price {args}:' + '\nNothing was found' + f"\n{'-'*10}\n"
            else:
                return found

    def findByCategoryId(self, categoryId, showMode=True):
        if type(categoryId) != int:
            raise TypeError('categoryId must be int type')
        # search
        found = []
        for product in self._products:
            if product.categoryId == categoryId:
                found.append(product)
        # output
        if showMode:
            if len(found) == 0:
                return f"\n{'-'*10}\n" + f'Products found by category id [{categoryId}]:' + f'\n\nNothing was found' + f"\n{'-'*10}\n"
            else:
                out = ''
                for product in found:
                    out = out + str(product)
                return f"\n{'-'*10}\n" + f'Products found by category id [{categoryId}]:' + out + f"\n{'-'*10}\n"
        else:
            return found

    def deleteById(self, id_):
        if type(id_) != int:
            raise TypeError('id must be int type')
        for product in self._products:
            if id_ == product.id:
                self._products.remove(product)
