from db.templates import *
from datetime import datetime


class Category(Model):
    def __init__(self, id_, name, parentCategoryId=None):
        self.inDB = False
        self.id = id_
        self.name = name
        self.parentCategoryId = parentCategoryId
        self.created = datetime.now()
        self.updated = None
    
    def __str__(self):
        title = f"--- Category \"{self.name}\" ---"
        id_ = f"Id: {self.id}"
        inDB = f'In DB: {self.inDB}'
        if self.parentCategoryId == None:
            parent = 'Have parent category: No'
        else:
            parent = 'Have parent category: Yes'
            parent = parent + '\n' + f'- parent categoty id: {self.parentCategoryId}'
        out = f'\n\n{title}\n{id_}\n{inDB}\n{parent}\n\n'
        return out
    
    def __repr__(self):
        return f'<<{[self.id, self.inDB, self.name, self.parentCategoryId]}>>'

    def __setattr__(self, name, value):
        if name == 'id':
            if self.inDB == False:
                if type(value) != int:
                    raise TypeError('id must have an int value')
        elif name == 'inDB':
            if value not in (True, False):
                raise TypeError(
                    'value for inDB attribute must be True or False only')
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
                        raise NameError('the name contains only the same letters')
                # Cheking name for numbers
                for letter in splited:
                    try:
                        int(letter)
                        raise NameError('the name must not contain integer values')
                    except ValueError:
                        pass
                object.__setattr__(self, name, value)
        elif name == 'parentCategoryId':
            if type(value) != int and value != None:
                raise TypeError('wrong parent Category id')
        elif name in ('created', 'updated'):
            if type(value) != datetime: raise TypeError('created or updated must have datetime object value')
        self.__setattr__('updated', datetime.now())
        object.__setattr__(self, name, value)

    def __eq__(self, other): return self.id == other.id if type(other) == Category else False


class CategoryRepositoryFactory(ModelRepositoryFactory):
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        res = self.pgds.query('SELECT id, name, parent_category_id FROM categories')
        if len(res) > 0:
            categories = []
            for row in res:
                c = self.get_category(row[0], row[1], row[2])
                c.inDB = True
                categories.append(c)
            out = ''
            for category in categories:
                out = out + str(category)
        else:
            out = '\nNo categories here\n'
        return out
    
    def __repr__(self):
        return str(self.pgds.query('SELECT * FROM categories'))

    # ##### Factory methods #####
    def get_category(self, id_, name, parentCategoryId=None):
        return Category(id_, name, parentCategoryId)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query('SELECT id, name, parent_category_id FROM categories')
        if len(res) > 0:
            categories = []
            for row in res:
                categories.append(self.get_category(row[0], row[1], row[2]))
            return categories
        else:
            return []
    
    def save(self, category):
        # Type verify
        if type(category) != Category:
            raise TypeError('the entity should only be Category type')
        # Save object data
        pcId = category.parentCategoryId
        if pcId == None:
            PcId = 'null'
        else:
            PcId = pcId
        if category.inDB == False:
            category.id = self.pgds.query(f'INSERT INTO categories(name, created, parent_category_id)\
                VALUES (\'{category.name}\', {category.created}, {PcId}) RETURNING id')[0][0]
            category.inDB = True
        elif category.inDB:
            self.pgds.query(f'''
                UPDATE categories
                SET name = \'{category.name}\',
                    updated = {category.updated},
                    parent_category_id = {PcId}
                WHERE id = {category.id}
            ''')

    def save_many(self, *categories):
        # Checking object quantity
        l = len(categories)
        if l in [0, 1]: raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(l):
            if type(categories[i]) != Category:
                raise TypeError(f'object number {i+1} is not a Category type')
        # Save objects data
        [self.save(category) for category in categories]
    
    def find_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int type')
        res = self.pgds.query(f'SELECT id, name, parent_category_id FROM categories WHERE id = {id_}')
        if len(res) != 0:
            data = res[0]
            c = self.get_category(data[0], data[1], data[2])
            c.inDB = True
            return c

    def delete_by_id(self, id_):
        if type(id_) != int: raise TypeError('id must be int type')
        self.pgds.query(f'DELETE FROM categories WHERE id = {id_}')
