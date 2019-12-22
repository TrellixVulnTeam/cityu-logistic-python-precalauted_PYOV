import csv
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from modelObjects.Edge import Edge
from Common import Common
import requests
import json
from utils.SingletonMetaclass import SingletonMetaclass
from dataset.NodeDataset import nodeDataset

class EdgeDataset(metaclass=SingletonMetaclass):
    def __init__(self):
        self.edges = {}
        self.nodesLink = {}
        self.loadingData()

    def loadingData(self,):
        path = 'data/road_link.csv'

        with open(path , encoding='utf-8-sig') as csvfile:
            readCSV = csv.reader(csvfile, delimiter='@')
            for row in readCSV:
                edge = Edge()
                edge.v_id = row[0]
                edge.osm_id = row[1]
                edge.type = row[2]
                edge.oneway = row[3]
                edge.maxspeed = row[4]
                edge.length = float(row[5])
                edge.name = row[6]
                edge.o_index = int(row[7])
                edge.d_index = int(row[8])
                edge.o_node = nodeDataset.findNodeById(edge.o_index)
                edge.d_node = nodeDataset.findNodeById(edge.d_index)
                self.edges[edge.v_id] = edge
                self.assignEdgeToStartNode(edge)

    def assignEdgeToStartNode(self,edge):
        o_index = edge.o_index

        if o_index not in self.nodesLink:
            self.nodesLink[o_index] = {}
        self.nodesLink[o_index][edge.d_index] = edge

    def getEdgeByStartPointAndEndPoint(self,o_index,d_index):
        return self.nodesLink[o_index][d_index]

    def getNodesByStartPoint(self,o_index):
        if o_index in self.nodesLink:
            return self.nodesLink[o_index]
        else:
            return {}
    def getEdgeById(self, edgeId):
        return self.edges[str(edgeId)]

edgeDataset = EdgeDataset()
print("Edge Dataset initialized")
# print(len(edgeDataset.nodesLink.keys()))
# print(len(edgeDataset.edges))