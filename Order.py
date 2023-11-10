from Node import Node
from Client import Client

class Order:
    def __init__(self, id, weight=0, volume=0, goods=[], street=Node(), time=0, client=Client()): # time é em minutos/segundos
        self.id = id
        self.weight = weight
        self.volume = volume
        self.goods = goods
        self.delivery_street = street
        self.delivery_time = time
        self.client = client

    def __str__(self):
        return "Order " + self.id + " To: " + self.client

    def __repr__(self):
        return "Order " + self.id + " To: " + self.client
    
    def getId(self):
        return self.id

    def getWeight(self):
        return self.weight
    
    def getVolume(self):
        return self.volume
    
    def getGoods(self):
        return self.goods
    
    def getStreet(self):
        return self.delivery_street
    
    def getTime(self):
        return self.delivery_time
    
    def getClient(self):
        return self.client
    
    def setId(self, newId):
        self.id = newId

    def setWeight(self, newWeight):
        self.weigth = newWeight
    
    def setVolume(self, newVolume):
        self.volume = newVolume
    
    def setGoods(self, newGoods):
        self.goods = newGoods

    def setStreet(self, newStreet):
        self.delivery_street = newStreet

    def setTime(self, newTime):
        self.delivery_time = newTime

    def setClient(self, newClient):
        self.client = newClient

    def __eq__(self, other):
        if other.isinstance(Order):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash(self.id)