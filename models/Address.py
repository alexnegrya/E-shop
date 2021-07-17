# Address.py module 

class Address:
    def __init__(self, id, country, city, street, number):
        self.setId(id)
        self.setCountry(country) 
        self.setCity(city)
        self.setStreet(street)
        self.setNumber(number)

    def __str__(self):
        return f"Id: {self._id}\nCountry: {self._country}\nCity: {self._city}\nStreet: {self._street}\nNumber: {self._number}"

    def __repr__(self):
        return str(self)
    
    ####### validation method adress parameter string type #######
    def __validateAddressName(self, name):
            if type(name) is not str:
                raise ValueError('Error: value must be string')
            if not name:
                raise ValueError('Error: value can\'t be empty')
            if len(name) < 3:
                raise ValueError("Error: country name is too short")


    def setId(self, id):
            if type(id) is not int:
                raise ValueError('Error: id must be integer')
            if id<=0 or id>1000000:
                raise ValueError("Error: id is not valid")
            self._id = id
    def getId(self):
        return self._id

    def setCountry(self, country):
            self.__validateAddressName(country)
            self._country = country

    def getCountry(self):
        return self._country

    def setCity(self, city):
            self.__validateAddressName(city)
            self._city = city
    def getCity(self):
        return self._city

    def setStreet(self, street):
            self.__validateAddressName(street)
            self._street = street
    def getStreet(self):
        return self._street

    def setNumber(self, number):
            if type(number) is not str:
                raise ValueError('Error: value must be string')
            if not number:
                raise ValueError('Error: value can\'t be empty')
            self._number = number
    def getNumber(self):
        return self._number

class AddressRepositoryFactory:
    def __init__(self):
        self.__lastCreatedId = 0
        self.__addresses = []

####### FACTORY methods #########
    def getAddress(self, country, city, street, number):
        id = self.__lastCreatedId + 1
        a = Address(id,country, city, street, number)
        self.__lastCreatedId = a.getId()
        ### remember the object in the list #####
        self.save(a)

        return a

####### REPOSITORY methods #########
# BREAD -> Browse, Read, Edit, Add, Delete
    def save(self,address):
        self.__addresses.append(address)

    def all(self):
        return tuple(self.__addresses)

    def findById(self, id):
        for p in self.__addresses:
            if p._id == id:
                return p
    def findByProperty(self, searchProperty):
        list_of_found = []
        for obj in self.__addresses:
            for name, value in obj.__dict__.items():
                if value == searchProperty:
                    list_of_found.append(obj)

            return list_of_found
            
    def deleteById(self, id):
        for obj in self.__addresses:
            for name, value in obj.__dict__.items():
                if value == id:
                    self.__addresses.remove(obj)