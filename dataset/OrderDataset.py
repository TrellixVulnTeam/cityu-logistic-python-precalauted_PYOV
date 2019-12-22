import csv
import os,sys,inspect
import random

from services.GraphService import graphService

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from modelObjects.Order import Order
from dataset.NodeDataset import nodeDataset
from Common import Common
import requests
import json
from utils.SingletonMetaclass import SingletonMetaclass
from dataset.EdgeDataset import edgeDataset
from utils.util import heuristicDistance,heuristicDistanceBetweenLatLng
import datetime

class OrderDataset(metaclass=SingletonMetaclass):
    def __init__(self):
        self.orders = []
        self.nonPlanedOrders = []
        self.deliveringOrders = []

    def getOrderByOrderId(self,orderId):
        return next((x for x in self.orders if x.orderId == orderId), None)


    def loadingData(self,date,path):


        with open(path, encoding='utf-8') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:

                order = Order()
                # targetNodeId = random.choice(graphService.subNodeIds)
                # targetNode = nodeDataset.findNodeById(targetNodeId)
                order.orderId = int(row[0])
                order.areaId = int(row[1])
                order.invoiceNo = str(row[2])
                order.invoiceCode = str(row[3])
                order.company = str(row[4])
                order.deliveryDate = date ##  row[5]
                order.clientName = str(row[6])
                order.clientPhone1 = str(row[7])
                order.clientPhone2 = str(row[8])
                order.lat = float(str(row[10]))
                order.lng = float(str(row[11]))
                order.productName = str(row[12])
                order.productNumber = int(row[13])
                order.capacity = int(str(row[14]))
                order.charge = 0
                order.categoryId = ""
                order.statusId = 0
                deliveryTimeStart = datetime.datetime.strptime(
                    "{} {}".format(date, str(row[21])),
                    "%Y-%m-%d %H:%M:%S")
                order.deliveryTimeStart = deliveryTimeStart
                deliveryTimeEnd = datetime.datetime.strptime("{} {}".format(date, str(row[22])),
                                                             "%Y-%m-%d %H:%M:%S")

                order.deliveryTimeEnd = deliveryTimeEnd
                nearestNode = graphService.findNearestVaildNode(order.lat,order.lng)
                order.setNearestNode(nearestNode)
                # print(order)
                # exit()
                self.orders.append(order)
        # self.orders = self.orders[:10]

        print("orderDataset.orders")
        print(orderDataset.orders)

        # for index in range(30):
        #     order = Order()
        #     targetNodeId = random.choice(graphService.subNodeIds)
        #     targetNode = nodeDataset.findNodeById(targetNodeId)
        #     order.orderId = targetNodeId
        #     order.areaId = ''
        #     order.invoiceNo = ""
        #     order.invoiceCode = ""
        #     order.company = ""
        #     order.deliveryDate = date
        #     order.clientName = ""
        #     order.clientPhone1 = ""
        #     order.clientPhone2 = ""
        #     order.lat = float(targetNode.lat)
        #     order.lng = float( targetNode.lng)
        #     order.productName = ""
        #     order.productNumber = ""
        #     order.capacity = 1
        #     order.charge = 0
        #     order.categoryId = ""
        #     order.statusId = 0
        #
        #     deliveryTimeStart = datetime.datetime.strptime(
        #         "{} {}".format(date, "10:00:00"),
        #         "%Y-%m-%d %H:%M:%S")
        #     order.deliveryTimeStart = deliveryTimeStart
        #     deliveryTimeEnd = datetime.datetime.strptime("{} {}".format(date, "18:00:00"),
        #                                                  "%Y-%m-%d %H:%M:%S")
        #     order.deliveryTimeEnd = deliveryTimeEnd
        #     nearestNode = self.getNearestNodeByOrder(order)
        #     order.setNearestNode(nearestNode)
        #     self.orders.append(order)
        # print("orderDataset.orders")
        # print(orderDataset.orders)


    def getNearestNodeByOrder(self,order):
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

orderDataset = OrderDataset()
print("Order Dataset initialized")


