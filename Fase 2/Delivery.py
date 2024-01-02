from Worker import worker
from Vehicles import Vehicle

class Delivery:
    current_id = 0
    def __init__(self, orders=[], worker=worker(), price=0.0, vehicle=Vehicle(), rating=0.0) -> None:
        Delivery.current_id += 1
        self.id = Delivery.current_id
        self.list_orders = orders # lista de objetos order
        self.worker = worker
        self.price = price
        self.vehicle = vehicle
        self.rating = rating

    def __str__(self):
        return "Delivery: " + self.id
    
    def getId(self):
        return self.id
    
    def getOrders(self):
        return self.list_orders
    
    def getWorker(self):
        return self.worker
    
    def getPrice(self):
        return self.price
    
    def getVehicle(self):
        return self.vehicle
    
    def getRating(self):
        return self.rating
    
    def setId(self, newId):
        self.id = newId

    def setOrders(self, newOrders):
        self.list_orders = newOrders

    def setWorker(self, newWorker):
        self.worker = newWorker

    def setPrice(self, newPrice):
        self.price = newPrice

    def setVehicle(self, newVehicle):
        self.vehicle = newVehicle

    def setRating(self, newRating):
        self.rating = newRating

    def __eq__(self, other):
        if other.isinstance(Delivery):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash(self.id)
                