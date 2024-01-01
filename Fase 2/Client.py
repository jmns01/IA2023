from Node import Node

class Client:
    def __init__(self, id, name="", history=[], street=Node()):
        self.id = id
        self.name = name
        self.order_history = history
        self.street = street

    def __str__(self) -> str:
        return "Client: " + self.id + " Name: " + self.name
    
    def getName(self):
        return self.name
    
    def getHistory(self):
        return self.order_history
    
    def getStreet(self):
        return self.street
    
    def setId(self, newId):
        self.id = newId

    def setName(self, newName):
        self.name = newName

    def setId(self, newHistory):
        self.order_history = newHistory

    def setId(self, newStreet):
        self.street = newStreet

    def __eq__(self, other):
        if other.isinstance(Client):
            return self.id == other.id and self.name == other.name
        return False
    
    def __hash__(self):
        return hash(self.name)