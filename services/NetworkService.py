import multiprocessing
import os, sys, inspect
import time
from multiprocessing.pool import ThreadPool

from dataset.DepotDataset import depotDataset
from dataset.OrderDataset import orderDataset

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from dataset.EdgeDataset import edgeDataset
from dataset.NodeDataset import nodeDataset
from dataset.DurationDataset import durationDataset
import networkx as nx
import random
from utils.SingletonMetaclass import SingletonMetaclass
import datetime
import numpy as np


class NetworkService(metaclass=SingletonMetaclass):
    def __init__(self, ):

        self.initGraph()
        # self.buildDynamicNetorkXNpz()

    def initGraph(self, ):
        self.G = nx.DiGraph()
        nodeIds = list(nodeDataset.nodes.keys())
        self.G.add_nodes_from(nodeIds)

        edges = []
        for startPoint in edgeDataset.nodesLink:
            for endPoint in edgeDataset.nodesLink[startPoint]:
                edge = edgeDataset.nodesLink[startPoint][endPoint]
                value = durationDataset.getStaticDurationByEdgeId(edge.v_id)
                edges.append((startPoint, endPoint, value))

        self.G.add_weighted_edges_from(edges)

    def buildDynamicNetorkXNpz(self,num):
        startDateTime = datetime.datetime.strptime("2019-11-25 09:30:00", "%Y-%m-%d %H:%M:%S")
        endDateTime = datetime.datetime.strptime("2019-11-25 19:00:00", "%Y-%m-%d %H:%M:%S")
        current = startDateTime
        count = 0
        self.timeArray = []
        while current < endDateTime:
            count += 1
            self.timeArray.append(current)
            newTime = current + datetime.timedelta(minutes=4)
            current = newTime

        orders = orderDataset.orders
        depot = depotDataset.depot
        orderNodes = (o.nearestNode.nodeId for o in orders)
        self.nodeSet = [depot.nearestNode.nodeId] + list(orderNodes)

        self.durationNp = np.zeros((len(self.timeArray), len(self.nodeSet), len(self.nodeSet)))

        print(self.durationNp.shape)
        for index in range(len(self.timeArray)):
            self.multiGraphicInit(index)
        np.savez("data/%s"%(num), nodeId=np.asarray(self.nodeSet), time=np.asarray(self.timeArray),
                 duration=self.durationNp)

    def multiGraphicInit(self, timelotIndex):
        print(timelotIndex)
        G = nx.create_empty_copy(self.G)
        edges = []
        for startPoint in edgeDataset.nodesLink:
            for endPoint in edgeDataset.nodesLink[startPoint]:
                edge = edgeDataset.nodesLink[startPoint][endPoint]
                value = durationDataset.getDynamicDurationByEdgeIdAndTime(edge.v_id, self.timeArray[timelotIndex])
                edges.append((startPoint, endPoint, value))
        G.add_weighted_edges_from(edges)

        for startIndex in range(len(self.nodeSet)):
            for endIndex in range(len(self.nodeSet)):
                if startIndex == endIndex:

                    self.durationNp[timelotIndex, startIndex, endIndex] = 0
                else:
                    startNodeId = self.nodeSet[startIndex]
                    endNodeId = self.nodeSet[endIndex]
                    self.durationNp[timelotIndex, startIndex, endIndex] = float(
                        nx.astar_path_length(G, startNodeId, endNodeId))

        # for node in nodes:


networkService = NetworkService()
