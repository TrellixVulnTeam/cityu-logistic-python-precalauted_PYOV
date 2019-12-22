import os,sys,inspect
import time

from utils.util import heuristicDistanceBetweenLatLng

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from dataset.EdgeDataset import edgeDataset
from dataset.NodeDataset import nodeDataset
from dataset.DurationDataset import durationDataset
import networkx as nx
import random
from utils.SingletonMetaclass import SingletonMetaclass
import datetime

class GraphService(metaclass=SingletonMetaclass):
    def __init__(self,):
        self.initGraph()
        self.getSubGraph()
        self.getAllPairDijkstraPathLength()
        self.staticNearestDuration = 0

    def initGraph(self,):
        self.G = nx.DiGraph()
        nodeIds=list(nodeDataset.nodes.keys())
        self.G.add_nodes_from(nodeIds)
        
        edges = []
        for startPoint in edgeDataset.nodesLink:
            for endPoint in edgeDataset.nodesLink[startPoint]:
                edge = edgeDataset.nodesLink[startPoint][endPoint]
                value = durationDataset.getStaticDurationByEdgeId(edge.v_id)
                edges.append((startPoint,endPoint,value))

        self.G.add_weighted_edges_from(edges)

    def getLargeNetwork(self):
        network = nx.strongly_connected_components(self.G)
        largest = max(network, key=len)
        return largest

    def getSubGraph(self):
        self.largestNodeSet = list(self.getLargeNetwork())

        currentConnectedSet = []
        # current = random.sample(largestSetId, 1)
        # currentConnectedSet.append(current[0])

        # currentConnectedSet.append(21714)
        # index = 0
        # while (len(currentConnectedSet) < 50):
        #     # print(currentConnectedSet[index])
        #     nextNodeSet = self.G.neighbors(currentConnectedSet[index])
        #     for key in nextNodeSet:
        #         if key not in currentConnectedSet:
        #             currentConnectedSet.append(key)
            # print(list(nextNodeSet.values()))
            # currentConnectedSet = currentConnectedSet + nextNodeSet
            # index += 1

        # H = self.G.subgraph(currentConnectedSet)
        # self.subNodeIds = currentConnectedSet
        # # print(currentConnectedSet)
        # print("SUB node %s" % len(self.subNodeIds))
        # print("SUB edge %s" % len(list(H.edges)))

    def getStaticDuration(self, startNodeId, nextNodeId):
        return float(nx.astar_path_length(graphService.G,startNodeId, nextNodeId))

    def getAllPairDijkstraPathLength(self):
        pass
        print("Running getAllPairDijkstraPathLength")
        # print(nx.astar_path_length(self.G, 7581, 11685))
        # length = nx.all_pairs_dijkstra_path_length(self.G)
        # print(list(length)[7581][11685])

    def findNearestVaildNode(self,lat,lng):
        distance = 10000
        currentNode = None
        for nodeId in self.largestNodeSet:
            node = nodeDataset.findNodeById(nodeId)
            tempDistance = heuristicDistanceBetweenLatLng(lat,lng,node.lat,node.lng)
            if distance >tempDistance:
                distance = tempDistance
                currentNode = node

        return currentNode



    def findNearestOrder(self,orders,selectedOrders):
        
        duration = 10000
        nearestOrder = None
        currentOrder = selectedOrders[-1]

        for order in orders:
            if order is not currentOrder and order not in selectedOrders:
                if nx.has_path(self.G,currentOrder.nearestNode.nodeId,order.nearestNode.nodeId)==False:
                    print("Not exist path from %s to %s" %(currentOrder.nearestNode.nodeId,order.nearestNode.nodeId))
                    exit()
                    # tempDuration =  3600
                else:
                    tempDuration = float(nx.astar_path_length(self.G,currentOrder.nearestNode.nodeId,order.nearestNode.nodeId))
                    # print("from %s to %s, static duration: %s" % (currentOrder.orderId, order.orderId,tempDuration))

                if tempDuration < duration:
                    duration = tempDuration
                    nearestOrder = order

        # print("selected nearestOrder %s" %(nearestOrder) )
        # exit()
        self.staticNearestDuration+=duration
        return nearestOrder



    def reStructureListByDuration(self, orders,depot):

        temp_no = random.randint(0,len(orders)-1)
        randomOrder = orders[temp_no]
        selectedOrders = []
        selectedOrders.append(depot)
        startTime = time.time()
        while(len(orders)>(len(selectedOrders)-1)):
            nearestOrder = self.findNearestOrder(orders,selectedOrders)
            selectedOrders.append(nearestOrder)
        del selectedOrders[0]


        crt_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("self.staticNearestDuration", self.staticNearestDuration)
        print("\nEnd restructureListByDuration: \ttime: %s\t%ds " % (crt_time, (time.time() - startTime)))

        # print(selectedOrders)
        # exit()
        return selectedOrders

graphService = GraphService()
