import csv
import os, sys, inspect

from dataset.OrderDataset import orderDataset

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from modelObjects.Node import Node
from Common import Common
import requests
import json
from utils.SingletonMetaclass import SingletonMetaclass


class DriverRecordDataset(metaclass=SingletonMetaclass):
    def __init__(self):
        self.driverRecords = {}
        # self.loadingData()

    def loadingData(self, path):
        # path = 'data/order1v.csv'
        with open(path, encoding='utf-8-sig') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            count =0
            for row in readCSV:
                if count ==0:
                    count+=1
                    continue
                # print(row)
                driverId = int(row[0])
                orderId = int(row[1])
                if driverId not in self.driverRecords:
                    self.driverRecords[driverId] = []
                order = orderDataset.getOrderByOrderId(orderId)
                if order ==None:
                    print("order:{} cannot find in order list".format(orderId))
                    raise
                self.driverRecords[driverId].append(order)
                # self.nodes[nodeId] = node

    # def findNodeById(self, nodeId):
    #     # return next((n for n in self.nodes if n.nodeId == nodeId), None)
    #     return self.nodes[nodeId]


driverRecordDataset = DriverRecordDataset()
# print(len(nodeDataset.nodes))
print("Node Dataset initialized")