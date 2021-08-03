class Category:
    __ids = []

    def __init__(self, name, parentCategoryId=None):
        self.id = self.__get_id()
        self.name = name
        self.parentCategoryId = parentCategoryId

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
        title = f"--- Category \"{self.name}\" ---"
        id = f"Id: {self.id}"
        if self.parentCategoryId == None:
            parent = 'Have parent category: No'
        else:
            parent = 'Have parent category: Yes'
            parent = parent + '\n' + f'- parent categoty id: {self.parentCategoryId}'
        out = '\n\n' + title + '\n' + id + '\n' + parent + '\n\n'
        return out
    
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
            if type(value) != int:
                raise TypeError('wrong parent Category id')
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
        if type(other) == Category:
            if self.id == other.id:
                return True
            else:
                return False


class CategoryRepositoryFactory:
    def __init__(self):
        self._lastCreatedId = 0
        self._categories = []

    def __str__(self):
        if len(self._categories) != 0:
            out = ''
            for category in self._categories:
                out = out + str(category)
        else:
            out = '\nThere are no categories here\n'
        return out
    
    def __repr__(self):
        return str(self)

    # ##### Factory methods #####
    def getCategory(self, name):
        obj = Category(name)
        self._lastCreatedId += 1
        obj.id = self._lastCreatedId
        self._categories.append(obj)
        return obj
    
    def get_last_id(self):
        return f"\n{'-'*10}\n" + 'Last created object id: ' + str(self._lastCreatedId) + f"\n{'-'*10}\n"

    # ##### Repository methods #####
    def all(self):
        return tuple(self._categories)
    
    def save(self, category):
        # Type verify
        if type(category) != Category:
            raise TypeError('the entity should only be Category type')
        # Id verify
        if len(self._categories) != 0:
            for c in self._categories:
                if category == c:
                    raise AttributeError('a Category object with this id already exists')
        self._categories.append(category)

    def save_many(self, categories_list):
        # checking categories_list type
        if type(categories_list) != list:
            raise TypeError('categories you want save should be in the list')
        # checking object quantity
        if len(categories_list) in [0, 1]:
            l = len(categories_list)
            raise ValueError(f'at least 2 objects can be saved, not {l}')
        # checking objects type
        for i in range(len(categories_list)):
            if type(categories_list[i]) != Category:
                raise TypeError(
                    f'object with index {i} is not a Category type')
        # checking objects id's
        for category in categories_list:
            for c in self._categories:
                if category.id == c.id:
                    raise AttributeError(
                        'a Category object with this id already exists')
        self._categories.extend(categories_list)

    def overwrite(self, categories_list):
        # checking categories_list type
        if type(categories_list) != list:
            raise TypeError(
                'categories you want overwrite should be in the list')
        # checking objects type
        for i in range(len(categories_list)):
            if type(categories_list[i]) != Category:
                raise TypeError(
                    f'object with index {i} is not a Category type')
        # checking objects id's
        for category in categories_list:
            for c in self._categories:
                if category.id == c.id:
                    raise AttributeError(
                        'a Category object with this id already exists')
        self._categories = categories_list
    
    def findById(self, id_, showMode=True):
        if type(id_) != int:
            raise TypeError('id must be int type')
        for category in self._categories:
            if category.id == id_:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Category found by id [{id_}]:' + str(category) + f"\n{'-'*10}\n"
                else:
                    return category
        if showMode:
            return f"\n{'-'*10}\n" + f'Category found by id [{id_}]:' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return category

    def findByName(self, name, showMode=True):
        if type(name) != str:
            raise TypeError('name must be str type')
        # With a incomplete match with the name
        found = []
        for category in self._categories:
            if name in category.name:
                found.append(category)
        if len(found) != 0:
            if showMode:
                out = ''
                for c in found:
                    out = out + str(c)
                return f"\n{'-'*10}\n" + f'Categories found by name keyword \"{name}\":' + out + f"\n{'-'*10}\n"
            else:
                return found
        # With a complete match with the name
        for category in self._categories:
            if category.name == name:
                if showMode:
                    return f"\n{'-'*10}\n" + f'Found Category with name \"{name}\":' + str(category) + f"\n{'-'*10}\n"
                else:
                    return found
        if showMode:
            return f"\n{'-'*10}\n" + f'Found Category with name \"{name}\":' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        else:
            return found

    def findByParentCategoryId(self, parentCategoryId, showMode=True):
        if type(parentCategoryId) != int:
            raise TypeError('parent category id must be int type')
        # search
        found = []
        for category in self._categories:
            if category.parentCategoryId == parentCategoryId:
                found.append(category)
        # output
        if showMode:
            if len(found) == 0:
                return f"\n{'-'*10}\n" + f'Categories found by parent category id [{parentCategoryId}]:' + f'\n\nNothing was found' + f"\n{'-'*10}\n"
            else:
                out = ''
                for category in found:
                    out = out + str(category)
                return f"\n{'-'*10}\n" + f'Categories found by parent category id [{parentCategoryId}]:' + out + f"\n{'-'*10}\n"
        else:
            return found

    def deleteById(self, id_):
        if type(id_) != int:
            raise TypeError('id must be int type')
        for category in self._categories:
            if id_ == category.id:
                self._categories.remove(category)
