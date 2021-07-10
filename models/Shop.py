import requests
#from Adress import Address

class Shop:
    
    def __init__(self, id, workingHours):
       
        self._id = id
        #self.addressId = self.addressId
        self.setWorkingHours(workingHours)  
        

    def setWorkingHours(self, workingHours):

       if type(workingHours) == None:
           raise ValueError("WorkingHours dictionary is empty!")

       else:
           self.workingHours = workingHours

            

    def getWorkingHours():
        return self._workingHours

    def __str__(self):
        return f"\n "\
               f" Shop id: {self.id}\n "\
               f" Working Hours: {self.workingHours}\n "

    def __repr__(self):
        return self.__str__()

class ShopRepositoryFactory:
    
    def __init__(self):
        self._lastCreatedId = 0
        self._shops = []


## FACTORY METHOD ####################
    def getShop (self, workingHours):

        obj = Shop(id, workingHours)
        self._lastCreatedId +=1
        obj.id = self._lastCreatedId
        # remember the obj ref in the list
        self.save (obj)

        return obj

## REPOSITORY METHOD #################
# BREAD -> Browse, Read, Edit, Add, Delete #####

    def save (self, shop):
        self._shops.append( shop )
    
    def all (self):
        return tuple(self._shops)

    def findById(self, id):

        for s in self._shops:
            if s.id == id:
                return s

    def findByworkingHour(self, workingHours):

        for s in self._shops:
            if s.workingHours == workingHours:
                
                    return s

    def deleteById(self, id):

        for s in self._shops:
            if s.id == id:
                self._shops.remove(s)
                return self._shops




