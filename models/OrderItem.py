

#OrderItem.py module


class OrderItem:
    
    def __init__( self, id, itemld, quantity ):
        
        self.id       = id
        self.itemld   = itemld
        self.quantity = quantity

    def __str__( self ):
        return f"{self.id} -- {self.itemld} -- {self.quantity}"

    def __repr__ ( self ):
        return f"{self.id} -- {self.itemld} -- {self.quantity}"

