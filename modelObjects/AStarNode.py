class AStarNode:
    def __init__(self,value,node):
        self.value = value
        self.node = node
        self.parent = None
        self.H = 0
        self.G = 0
        self.timeSlot = None
        self.edge = -1
        self.edgeId = -1

    def __repr__(self):
        return "EdgeId : {} ,Lat : {}, lng : {}, value cost {}, total cost : {}, timeSlot : {}".format(self.edgeId,self.node.lat,self.node.lng,self.value,self.G,self.timeSlot)
