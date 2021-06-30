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
        out = '\n' + title + '\n' + id + '\n' + parent + '\n'
        return out
    
    def __repr__(self):
        return str(self)

    def __setattr__(self, name, value):
        if name == 'id':
            if value < 1 or value > 1000000:
                raise ValueError('id must be greater then 0 and lesser then 1000000')
            else:
                object.__setattr__(self, name, value)