

#OrderItem.py module
from random import randint


class OrderItem:
    
    
    def __init__( self, _id, itemld, quantity ):
       
        if _id in range( 1, 1_000_000 + 1 ):
            self.id = _id
        
        else:
            raise ValueError( "id out of range" )

        self.itemld   = itemld
        self.quantity = quantity


    def __str__( self ):
        return f"{self.id} -- {self.itemld} -- {self.quantity}"

    def __repr__ ( self ):
        return self.__str__()
    
