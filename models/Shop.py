

from Adress import Address




class Shop:
    
    def __init__(self, shopID, addressID, workingHours):
        self.shopID = shopID
        
        if shopID >= 1 and shopID < 1000000:

                self.addressID = addressID
        else:
                raise ValueError ("Error!!! You reach the max. number of records!!!")
        self.workingHours = workingHours

        
        



    def __str__(self):
        return f"{self.shopID}, {self.addressID}, {self.workingHours}"

    def __repr__(self):
        return self.__str__()


