class Category:
    def __init__(self, name, parentCategoryId=None):
        if type(name) == str:
            self.name = name
        else:
            raise TypeError('wrong name type')
        if parentCategoryId != None:
            if type(parentCategoryId) == str:
                self.parentCategoryId = parentCategoryId
            else:
                raise TypeError('wrong parentCategoryId type')
        else:
            self.parentCategoryId = None
    
    def __str__(self):
        title = f"--- Category \"{self.name}\" ---"
        if self.parentCategoryId == None:
            parent = 'Have parent category: No'
        else:
            parent = 'Have parent category: Yes'
            parent = parent + '\n' + f'- parent categoty id: {self.parentCategoryId}'
        out = title + '\n' + parent
        return out
    
    def __repr__(self):
        return str(self)