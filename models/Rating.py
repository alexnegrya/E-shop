from Customer import *
from Product import *




class Rating:
    def __init__(self, _id, _name, customerId, _stars, review):
        self._id = _id
        self._name = _name
        self.customerId = customerId
        self._stars = _stars
        self.review = review



    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if 0 <= int(value) < 1000000:
            return True
        if not isinstance(value, int):
                raise TypeError("Only numbers are allowed ")
        else:
            raise ValueError("ID must be between 1 and 1 000 000")

        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        for n in value:
            if n.isdigit():
                raise TypeError("Enter valid product name")
        self.__name = value

    @property
    def stars(self):
        return self.__stars

    @stars.setter
    def stars(self, value):
        if 0 <= value <= 5:
            return True
        if not isinstance(value, int):
            raise TypeError("Only numbers are allowed ")
        else:
            raise ValueError("ID must be between 1 and 5")

        self.__stars = value


    def __str__(self):
        return f"\n " \
               f"Product ID : {self._id}\n " \
               f"Name  : {self._name}\n " \
               f"{self.customerId}\n " \
               f"Rating: {self._stars}\n " \
               f"Rewiew: {self.review}\n "

    def __repr__(self):
        return str(self)



class RatingRepositoryFactory:
    def __init__(self):
        self._lastCreatedId = 0
        self._products = []

    # Factory methods
    def getReview(self, _name, customerId, _stars, review):
        rew = Rating(id, _name, customerId, _stars, review)
        self._lastCreatedId = +1
        rew._id = self._lastCreatedId

        # remember the obj ref in the list
        self.save(rew)

        return rew

    # Repository methods
    # BREAD -> Browse, Read, Edit, Add, Delete
    def save(self, product):
        self._products.append(product)

    def all(self):
        return tuple(self._products)

    def findById(self, _id):
        for p in self._products:
            if p._id == _id:
                return p
            
    def findByStars(self, _stars):
        
        for s in self._products:
            if s._stars == _stars:
                return s

    def deleteById(self, _id):
        for product in self._products:
            if product._id == _id:
                self._products.remove(product)       

