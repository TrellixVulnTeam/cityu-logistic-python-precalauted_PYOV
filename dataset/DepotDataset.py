import os,sys,inspect

from services.GraphService import graphService

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from modelObjects.Depot import Depot
from dataset.NodeDataset import nodeDataset
from utils.SingletonMetaclass import SingletonMetaclass
from dataset.EdgeDataset import edgeDataset
from utils.util import heuristicDistance
from Common import Common
import datetime
import requests,json

class DepotDataset(metaclass=SingletonMetaclass):

    def __init__(self):

        pass


    def loadingData(self,):
        # path = Common.apiPath + "depots/get";
        # r = requests.post(path)
        #
        # row=json.loads(r.text)

        depot = Depot()
        depot.lat =float(22.3668065)
        depot.lng =float(114.13775780000003)
        depot.address="葵涌和宜合道57-61號裕華貨倉大廈四樓"
        depot.capacity = int(1)

        depot.deliveryTimeStart =Common.startTimeWindow
        depot.deliveryTimeEnd =Common.endTimeWindow
        nearestNode = graphService.findNearestVaildNode(depot.lat,depot.lng)
        depot.setNearestNode(nearestNode)
        self.depot = depot

    def getNearestNode(self,order):
        minDistance = 10000
        currentNode = nodeDataset.nodes[5000]

        for edgeId in edgeDataset.edges:
            edge = edgeDataset.edges[edgeId]

            distance = heuristicDistance(order,edge.o_node)
            if distance < minDistance:
                minDistance = distance
                currentNode = edge.o_node
            distance = heuristicDistance(order,edge.d_node)
            if distance < minDistance:
                minDistance = distance
                currentNode = edge.d_node
        return currentNode

depotDataset = DepotDataset()
print("Depot Dataset initialized")