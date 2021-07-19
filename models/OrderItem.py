

#OrderItem.py module
from random import randint


class OrderItem:
    
    
    def __init__( self, _id, _itemld, _quantity ):
       
#        if id in range( 0, 1_000_000 + 1 ):
        self.setId( _id )
        
#        else:
#            raise ValueError( "id out of range" )

        self.setItemld( _itemld )
        self.setQuantity( _quantity )
    

    def setId( self, id ):
        self._id = id
    
    def getId( self, id ):
        return self._id


    def setItemld( self, itemld ):
        self._itemld = itemld

    
    def getItemld( self, itemld ):
        return self._itemld

    
    
    def setQuantity( self, quantity ):
        if quantity <= 0:
            raise ValueError( "Quantity can't be 0 or negative!" )
        
        self._quantity = quantity

    
    def getQuantity( self, quantity ):
        return self._quantity

    
    
    def __str__(self):
        return f"item id: {self._id:6}; {self._itemld:12} X {self._quantity}"

    def __repr__ ( self ):
        return self.__str__()

class OrderItemRepositoryFactory:

#FACTORY METHODS ####################
    
    def __init__( self ):
        self._lastCreatedId = 0
        self._orderItems = []

    def getOrderItem( self, itemld, quantity ):
        obj = OrderItem( id, itemld, quantity )
        self._lastCreatedId += 1
        obj._id = self._lastCreatedId

	#remember the obj ref in the list
        self.save( obj )
        return obj  


#REPOSITORY METHODS ####################

    def save( self, orderItem, quantity ):
        if orderItem in self._orderItems:
            raise ValueError( "The same item is already in list!" )
        
        self._orderItems.append( orderItem )


    def all( self ):
        return tuple(self._orderItems)

    def findById( self, id ):
        for i in self._orderItems:
            if( i._id == id ):
                return i
        return None        

    def findByItemld( self, itemld ):
        for i in self._orderItems:
            if( i._itemld == itemld ):
                return i
        return None        











