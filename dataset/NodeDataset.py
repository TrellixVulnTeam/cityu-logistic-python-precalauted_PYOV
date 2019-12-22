import csv
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from modelObjects.Node import Node
from Common import Common
import requests
import json
from utils.SingletonMetaclass import SingletonMetaclass

class NodeDataset(metaclass=SingletonMetaclass):
    def __init__(self):
        
        self.nodes = {}
        self.loadingData()

    def loadingData(self):
        path = 'data/road_nodes.csv'
        with open(path , encoding='utf-8-sig') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                # print(row)
                nodeId = int(row[0])
                lat, lng = float(row[1]), float(row[2])
                node = Node(nodeId, lat, lng)
                self.nodes[nodeId] = node

    def findNodeById(self,nodeId):
        # return next((n for n in self.nodes if n.nodeId == nodeId), None)
        return self.nodes[nodeId]
nodeDataset = NodeDataset()
# print(len(nodeDataset.nodes))
print("Node Dataset initialized")