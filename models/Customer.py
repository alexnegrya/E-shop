class Customer:
    def __init__(self, id, firstName, lastName, addressId):
        self.__id = id
        self.firstName = firstName
        self.lastName = lastName
        self.addressId = addressId

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        if id in range(1, 1000000):
            self.__id = id
        else:
            raise ValueError ("Enter a range of values from 1 to 1 000 000")
    def __str__(self):
        return f"\nID customer: {self.__id}\nFirst name: {self.firstName}\nLast name: {self.lastName}\nAdress Id: {self.addressId}"
    
    def __repr__(self):
       return self.__str__()

############# Factory Repository Method ################

class CustomerRepositoryFactory:
    def __init__ (self):
        self._lastCreatedId = 0
        self._customers = []

################# Factory Method ######################

    def getCustomer(self, firstName, lastName, addressId):
        obj = Customer(id, firstName, lastName, addressId)
        self._lastCreatedId += 1
        obj.id = self._lastCreatedId
        self.save(obj)
        return obj
