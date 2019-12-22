from multiprocessing.pool import ThreadPool
import os, sys, inspect

from dataset.PreComputedDataset import preComputedDataset
from excpetions.TimeWindowExceeded import TimeWindowExceeded
from services.AStarService import aStarService

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import networkx as nx
from services.GraphService import graphService
import datetime
from utils.SingletonMetaclass import SingletonMetaclass
import time


# from services.CPDService import cPDService
class TravellingService(metaclass=SingletonMetaclass):

    def __init__(self, ):
        self.method = 0
        self.cahces = {}
        print('TravellingService Init')


    def calucateTravelNodeFromDeliveryList(self, singleDeliveryList, startTimeWindow, endTimeWindow):
        self.startTimeWindow = startTimeWindow
        self.endTimeWindow = endTimeWindow
        key = "";
        for delivery in singleDeliveryList:
            key += ","+ str(delivery.order.orderId)

        if key not in self.cahces:
            try:
                singleDeliveryList = self.doCalucateTravelNode(singleDeliveryList)
                self.cahces[key] = singleDeliveryList
            except TimeWindowExceeded:
                # self.cahces[key] = "err"
                raise TimeWindowExceeded
        else:
            singleDeliveryList = self.cahces[key]
            if singleDeliveryList == "err":
                raise TimeWindowExceeded
            # print("Existing Key %s" %(key))
        return singleDeliveryList

    def doCalucateTravelNode(self,singleDeliveryList):
            if len(singleDeliveryList) == 2:
                singleDeliveryList[0].deliveryTime = self.startTimeWindow
                singleDeliveryList[1].deliveryTime = self.startTimeWindow
                return singleDeliveryList


            for index in range(len(singleDeliveryList) - 1):
                startDelivery = singleDeliveryList[index]
                if index == 0:
                    startDelivery.deliveryTime = self.startTimeWindow
                endDelivery = singleDeliveryList[index + 1]
                fromNode = startDelivery.order.nearestNode
                toNode = endDelivery.order.nearestNode
                start_time = time.time()
                if nx.has_path(graphService.G, fromNode.nodeId, toNode.nodeId) == False:
                    print('No path {}, {}'.format(fromNode, toNode))
                else:
                    if self.method == 0 :
                        value = preComputedDataset.getDynamicDurationByNodeIdsAndTime(startDelivery.order.nearestNode.nodeId, endDelivery.order.nearestNode.nodeId,startDelivery.deliveryTime + datetime.timedelta(
                                                      seconds=startDelivery.serviceTime))
                        # print(value)
                        # exit()
                        # nodeList,_ = aStarService.doSearch(startDelivery.order.nearestNode, endDelivery.order.nearestNode,
                        #                           startDelivery.deliveryTime + datetime.timedelta(
                        #                               seconds=startDelivery.serviceTime))

                    # endDelivery.aStarNodeList = nodeList
                    # print(nodeList)
                    travelTime = value
                    # lastAStarNodeDeliveryTime = nodeList[-1].timeSlot
                    endDelivery.deliveryTime = startDelivery.deliveryTime + datetime.timedelta(
                        seconds=(startDelivery.serviceTime + travelTime))
                    if endDelivery.deliveryTime < endDelivery.order.deliveryTimeStart or (endDelivery.deliveryTime + datetime.timedelta(seconds=endDelivery.serviceTime) > endDelivery.order.deliveryTimeEnd):
                        raise TimeWindowExceeded


            return singleDeliveryList


    def calucateTravelNodeFromDeliveryListWithOutWindowLimit(self, singleDeliveryList, startTimeWindow, endTimeWindow):
        self.startTimeWindow = startTimeWindow
        self.endTimeWindow = endTimeWindow
        key = "";
        print(singleDeliveryList)
        for delivery in singleDeliveryList:
            print(delivery)
            key += ","+ str(delivery.order.orderId)

        if key not in self.cahces:
            try:
                singleDeliveryList = self.doCalucateTravelNodeWithOutWindowLimit(singleDeliveryList)
                self.cahces[key] = singleDeliveryList
            except TimeWindowExceeded:
                # self.cahces[key] = "err"
                raise TimeWindowExceeded
        else:
            singleDeliveryList = self.cahces[key]
            if singleDeliveryList == "err":
                raise TimeWindowExceeded
            # print("Existing Key %s" %(key))
        return singleDeliveryList

    def doCalucateTravelNodeWithOutWindowLimit(self,singleDeliveryList):
            if len(singleDeliveryList) == 2:
                singleDeliveryList[0].deliveryTime = self.startTimeWindow
                singleDeliveryList[1].deliveryTime = self.startTimeWindow
                return singleDeliveryList


            for index in range(len(singleDeliveryList) - 1):
                startDelivery = singleDeliveryList[index]
                if index == 0:
                    startDelivery.deliveryTime = self.startTimeWindow
                endDelivery = singleDeliveryList[index + 1]
                fromNode = startDelivery.order.nearestNode
                toNode = endDelivery.order.nearestNode
                start_time = time.time()
                if nx.has_path(graphService.G, fromNode.nodeId, toNode.nodeId) == False:
                    print('No path {}, {}'.format(fromNode, toNode))
                else:
                    if self.method == 0 :
                        value = preComputedDataset.getDynamicDurationByNodeIdsAndTime(startDelivery.order.nearestNode.nodeId, endDelivery.order.nearestNode.nodeId,startDelivery.deliveryTime + datetime.timedelta(
                                                      seconds=startDelivery.serviceTime))
                        # print(value)
                        # exit()
                        # nodeList,_ = aStarService.doSearch(startDelivery.order.nearestNode, endDelivery.order.nearestNode,
                        #                           startDelivery.deliveryTime + datetime.timedelta(
                        #                               seconds=startDelivery.serviceTime))

                    # endDelivery.aStarNodeList = nodeList
                    # print(nodeList)
                    travelTime = value
                    # lastAStarNodeDeliveryTime = nodeList[-1].timeSlot
                    endDelivery.deliveryTime = startDelivery.deliveryTime + datetime.timedelta(
                        seconds=(startDelivery.serviceTime + travelTime))
                    # if endDelivery.deliveryTime < endDelivery.order.deliveryTimeStart or (endDelivery.deliveryTime + datetime.timedelta(seconds=endDelivery.serviceTime) > endDelivery.order.deliveryTimeEnd):
                    #     raise TimeWindowExceeded


            return singleDeliveryList



travellingService = TravellingService()