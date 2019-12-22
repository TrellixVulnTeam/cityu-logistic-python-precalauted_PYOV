
class Node:
    def __init__(self,nodeId, lat, lng):
        self.nodeId = nodeId
        self.lat = lat
        self.lng = lng
    

    def getLatLng(self):
    	return str(self.lat) +',' + str(self.lng)

    def __repr__(self):
        return "Node {}: ({},{})".format(self.nodeId,self.lat,self.lng)
