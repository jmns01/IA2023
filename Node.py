
# O Mapa vai ser do tipo:
# Rua1 Rua2 Rua3
# Rua4 Rua5 Rua6
# Rua7 Rua8 Rua9
#      Rua10
#



class Node: # Ou rua
    def __init__(self, name, id, length=0, lista=[], cortada=False, transito=False):
        self.m_id = id
        self.m_name = str(name)
        self.street_length = length # Este deve ser ajustado no add_edge()
        self.adjacent_streets = lista # Aqui deve ficar o nome (str) das ruas adjacentes
        self.cortada = cortada # Estes valores são ligados aleatóriamente
        self.transito = transito

    def __str__(self):
        return "node " + self.m_name + " Cortada? " + str(self.cortada) + " Transito? " + str(self.transito)

    def __repr__(self):
        return "node " + self.m_name

    def getId(self):
        return self.m_id
    
    def setId(self, id):
        self.m_id = id

    def getName(self):
        return self.m_name
    
    def setName(self, name):
        self.m_name = name
    
    def getStreetLength(self):
        return self.street_length
    
    def setStreetLegnth(self, newLength):
        self.street_length = newLength

    def getAdjancents(self):
        return self.adjacent_streets
    
    def setAdjacents(self, newAdj):
        self.adjacent_streets = newAdj

    def getCortada(self):
        return self.cortada
    
    def setCortada(self, newCortada):
        self.cortada = newCortada

    def getTransito(self):
        return self.transito
    
    def setTransito(self, newTransito):
        self.transito = newTransito

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.m_name == other.m_name
        return False
    
    def __hash__(self):
        return hash(self.m_name)