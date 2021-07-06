from random import randint

class Category:
    def __init__(self, name, parentCategoryId=None):
        ID = ''
        for v in range(randint(4, 6)):
            ID = ID + str(randint(0, 9))
        self.id = int(ID)
        self.name = name
        self.parentCategoryId = parentCategoryId
    
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
            if value < 1 or value > 1000000:
                raise ValueError('id must be greater then 0 and lesser then 1000000')
            elif type(value) != int:
                raise TypeError('id must be an integer')
            else:
                object.__setattr__(self, name, value)
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
                repeat_numbers = {}
                for i in range(len(splited)):
                    if splited[i] not in repeat_numbers:
                        repeat_numbers[splited[i]] = 1
                    else:
                        repeat_numbers[splited[i]] += 1
                # Checking name for the same letters only
                for i in range(len(repeat_numbers)):
                    if repeat_numbers[splited[i]] == len(value):
                        raise NameError('the name contains only the same letters')
                # Cheking name for numbers
                for letter in splited:
                    try:
                        int(letter)
                        raise NameError('the name must not contain integer values')
                    except ValueError:
                        pass
                object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)
    
    def __getattr__(self, name):
        if name == 'id':
            return str(self._id)
    
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
            raise TypeError('the entity should only be of the Category type')
        # Id verify
        if len(self._categories) != 0:
            for c in self._categories:
                if category == c:
                    raise AttributeError('a Category object with this id already exists')
        self._categories.append(category)
    
    def findById(self, id_):
        for category in self._categories:
            if category.id == id_:
                return f"\n{'-'*10}\n" + f'Category found by id [{id_}]' + str(category) + f"\n{'-'*10}\n"
        return f"\n{'-'*10}\n" + f'Category found by id [{id_}]' + '\n\nNothing was found' + f"\n{'-'*10}\n"
    
    def findByName(self, name):
        # With a incomplete match with the name
        found = []
        for category in self._categories:
            if name in category.name:
                found.append(category)
        if len(found) != 0:
            out = ''
            for c in found:
                out = out + str(c)
            return f"\n{'-'*10}\n" + f'Categories found by keyword \"{name}\"' + out + f"\n{'-'*10}\n"
        else:
            return f"\n{'-'*10}\n" + f'Categories found by keyword \"{name}\"' + '\n\nNothing was found' + f"\n{'-'*10}\n"
        # With a complete match with the name
        for category in self._categories:
            if category.name == name:
                return f"\n{'-'*10}\n" + f'Found Category with name \"{name}\":' + str(category) + f"\n{'-'*10}\n"
        return f"\n{'-'*10}\n" + f'Found Category with name \"{name}\":' + '\n\nNothing was found' + f"\n{'-'*10}\n"

    def deleteById(self, id_):
        for category in self._categories:
            if id_ == category.id:
                self._categories.remove(category)
