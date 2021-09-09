class Category:
    def __init__(self, id_, name, parentCategoryId=None):
        self.inDB = False
        self.id = id_
        self.name = name
        self.parentCategoryId = parentCategoryId
    
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
                if type(value) == int:
                    object.__setattr__(self, name, value)
                else:
                    raise TypeError('id must have an int value')
        elif name == 'inDB':
            if value in (True, False):
                object.__setattr__(self, name, value)
            else:
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
            else:
                object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def __eq__(self, other):
        if type(other) == Category:
            if self.id == other.id:
                return True
            else:
                return False


class CategoryRepositoryFactory:
    def __init__(self, pgds):
        self.pgds = pgds

    def __str__(self):
        res = self.pgds.query('SELECT id, name, parent_category_id FROM categories')
        if len(res) > 0:
            categories = []
            for row in res:
                c = self.getCategory(row[0], row[1], row[2])
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
    def getCategory(self, id_, name, parentCategoryId=None):
        return Category(id_, name, parentCategoryId)

    # ##### Repository methods #####
    def all(self):
        res = self.pgds.query('SELECT id, name, parent_category_id FROM categories')
        if len(res) > 0:
            categories = []
            for row in res:
                categories.append(self.getCategory(row[0], row[1], row[2]))
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
                VALUES (\'{category.name}\', now(), {PcId}) RETURNING id')[0][0]
            category.inDB = True
        elif category.inDB:
            self.pgds.query(f'''
                UPDATE categories
                SET name = \'{category.name}\',
                    updated = now(),
                    parent_category_id = {PcId}
                WHERE id = {category.id}
            ''')

    def save_many(self, *categories):
        # Checking object quantity
        l = len(categories)
        if l in [0, 1]:
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # Checking objects type
        for i in range(len(categories)):
            if type(categories[i]) != Category:
                raise TypeError(f'object number {i+1} is not a Category type')
        # Save objects data
        for category in categories:
            pcId = category.parentCategoryId
            if pcId == None:
                PcId = 'null'
            else:
                PcId = pcId
            if category.inDB == False:
                category.id = self.pgds.query(f'INSERT INTO categories(name, created, parent_category_id)\
                VALUES (\'{category.name}\', now(), {PcId}) RETURNING id')[0][0]
                category.inDB = True
            elif category.inDB:
                self.pgds.query(f'''
                    UPDATE categories
                    SET name = \'{category.name}\',
                        updated = now(),
                        parent_category_id = {PcId}
                    WHERE id = {category.id}
                ''')
    
    def findById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Search
        res = self.pgds.query(f'SELECT id, name, parent_category_id FROM categories WHERE id = {id_}')
        if len(res) != 0:
            data = res[0]
            c = self.getCategory(data[0], data[1], data[2])
            c.inDB = True
            return c

    def deleteById(self, id_):
        # Checking type
        if type(id_) != int:
            raise TypeError('id must be int type')
        # Delete object data
        self.pgds.query(f'DELETE FROM categories WHERE id = {id_}')
