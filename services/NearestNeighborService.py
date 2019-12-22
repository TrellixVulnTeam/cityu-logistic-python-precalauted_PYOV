import os, sys, inspect
from multiprocessing.pool import ThreadPool

from dataset.OrderDataset import orderDataset
from dataset.PreComputedDataset import preComputedDataset
from excpetions.TimeWindowExceeded import TimeWindowExceeded
from modelObjects.Delivery import Delivery
from services.TravellingService import travellingService
from utils.util import heuristicDistanceBetweenLatLng

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from services.AStarService import aStarService
from services.EnvironmentService import environmentService
from Common import Common
from utils.SingletonMetaclass import SingletonMetaclass
from services.GraphService import graphService
import copy
import random
from modelObjects.FitnessObject import FitnessObject

import time


class NearestNeighborService(metaclass=SingletonMetaclass):
    def __init__(self):
        pass


    def findDriverVehicleOrderList(self):

        totalDriverVehicleList = []
        remainOrderList = orderDataset.orders[:]
        selectedOrderList = []
        for i in range(len(environmentService.driverVehicles)):
            currentDriverVehiceList = []
            for index in range(len(remainOrderList)):
                if index  ==0:
                    currentTime = environmentService.depot.deliveryTimeStart
                    currentOrder = environmentService.depot
                nearestOrders = self.findNearestOrderList(currentOrder,remainOrderList, selectedOrderList, currentTime)
                for order in nearestOrders:
                    tempTestPath = copy.deepcopy(currentDriverVehiceList)
                    tempTestPath.append(order)
                    signleDeliveriesList = environmentService.orderListToMutliDeliveriesList(tempTestPath)
                    valid, newMutliDeliveriesList = self.checkSingleValidFromTempPath(signleDeliveriesList)
                    # print(valid)
                    if valid ==True:
                        # print(order)
                        latestDelivery = newMutliDeliveriesList[0][-2]
                        currentTime = latestDelivery.deliveryTime
                        currentOrder = order
                        selectedOrderList.append(currentOrder)
                        currentDriverVehiceList = tempTestPath
                        print("add currentOrder %s:"%currentOrder)
                        del remainOrderList[remainOrderList.index(order)]
                        break
                    else:
                        print(newMutliDeliveriesList)
            if len(currentDriverVehiceList)>0:
                vaildPath = currentDriverVehiceList
                vaildPath.append(environmentService.depot)
                totalDriverVehicleList = totalDriverVehicleList + vaildPath

            if len(remainOrderList) ==0:
                break


        remainDeliveryDriverList = self.considerTimewindowWaitingTIme(remainOrderList)
        totalDeliveryList = environmentService.orderListToMutliDeliveriesList(totalDriverVehicleList)
        updatedDeliveryList  = []
        for singleDeliveryList in totalDeliveryList:
            if len(singleDeliveryList) >2:
                updatedDeliveryList.append(singleDeliveryList)

        updatedDeliveriesList = updatedDeliveryList + remainDeliveryDriverList
        # updatedTotalVehicleList = updatedTotalVehicleList + remainOrderDriverList
        vehicleCount = len(updatedDeliveriesList)
        driverVehiclesLength = len(environmentService.driverVehicles)

        if vehicleCount > driverVehiclesLength-1:
            print(updatedDeliveriesList)
            print("Not enough vehicle")
            print("max vehicle size %s" % driverVehiclesLength )
            print("Using vehicle size %s" % vehicleCount)

        print('success')
        # print(len(updatedDeliveriesList))
        # exit()
        # for index in range(vehicleCount,driverVehiclesLength-1):
        #     updatedTotalVehicleList.append(environmentService.depot)
        return updatedDeliveriesList

    def findNearestOrderList(self, currentOrder, nonSelectedorders, selectedOrders, currentTime):

        nearestOrderList = {}

        for order in nonSelectedorders:
            if order is not currentOrder and order not in selectedOrders:
                tempDuration = preComputedDataset.getDynamicDurationByNodeIdsAndTime(currentOrder.nearestNode.nodeId,order.nearestNode.nodeId, currentTime)
                nearestOrderList[tempDuration] = order
        nearestOrderArray = []
        for key in sorted(nearestOrderList.keys()):
            nearestOrderArray.append(nearestOrderList[key])

        return nearestOrderArray

    def checkSingleValidFromTempPath(self, signleDeliveriesList):

        vaild = environmentService.isSingleOrderCapacityVaild(signleDeliveriesList)

        if vaild == False:
            return False, "FALSE Capacity"

        newMutliDeliveriesList = []
        try:
            newMutliDeliveriesList.append(
                travellingService.calucateTravelNodeFromDeliveryList(signleDeliveriesList[0], signleDeliveriesList[0][0].order.deliveryTimeStart,
                                                                         signleDeliveriesList[0][-1].order.deliveryTimeEnd))
        except:
            # print("FALSE Time Windows 1")
            return False, "FALSE Time Windows 1"
        # print(newMutliDeliveriesList)
        # latestDelivery = newMutliDeliveriesList[0][-2]

        vaild = environmentService.isTimeWindowsVaild(newMutliDeliveriesList)
        if vaild == False:
            return False, "Time window 2 False"
        return True, newMutliDeliveriesList

    def checkValidFromTempPath(self, tempPath):
        mutliDeliveriesList = environmentService.orderListToMutliDeliveriesList(tempPath)
        vaild = environmentService.isOrderStructureValid(mutliDeliveriesList)

        if vaild == False:
            return False, None

        newMutliDeliveriesList = []
        try:
            pool = random.sample(mutliDeliveriesList, len(mutliDeliveriesList))
            for singleDelivery in pool:
                newMutliDeliveriesList.append(
                    travellingService.calucateTravelNodeFromDeliveryList(singleDelivery, singleDelivery[0].order.deliveryTimeStart,
                                                                         singleDelivery[-1].order.deliveryTimeEnd))
        except TimeWindowExceeded:
            return False, None

        vaild = environmentService.isTimeWindowsVaild(newMutliDeliveriesList)
        if vaild == False:
            return False, None
        return True, newMutliDeliveriesList



    def run(self, num):

        print("Starting Running NearestNeighborService")
        nearestDriverVehilceList = self.findDriverVehicleOrderList()
        newMutliDeliveriesList = []
        for singleDelivery in nearestDriverVehilceList:
            newMutliDeliveriesList.append(
                travellingService.calucateTravelNodeFromDeliveryList(singleDelivery,
                                                                     singleDelivery[0].order.deliveryTimeStart,
                                                                     singleDelivery[-1].order.deliveryTimeEnd))

        self.nearestDriverVehilceList = nearestDriverVehilceList
        # print(self.nearestDriverVehilceList)
        # exit()
        finessobject = FitnessObject(nearestDriverVehilceList,newMutliDeliveriesList)

        finessobject.routeFitness()

        nCsv = open('./result/%s_nn.csv'%num, 'a+', encoding='utf-8-sig')
        nCsv.write("Total vehicle: %s\n" %finessobject.vehicleNum)
        nCsv.write("TotalDuration: %ss\n" %finessobject.totalDuration)
        nCsv.write("TotalTravelDuration: %ss\n" % (finessobject.totalDurationWithoutNonUseVehicle - finessobject.totalServiceTime))
        nCsv.close()
        return finessobject

    def considerTimewindowWaitingTIme(self, remainOrderList):
        print("remainOrderList",len(remainOrderList))
        sortedStartTimeOrderList = sorted(remainOrderList, key=lambda x: x.deliveryTimeStart)
        totalDriverList = []
        currentList = sortedStartTimeOrderList
        timeWindowCount = 0
        firstOrder = None
        while len(currentList)!=0:
            deliveriesList = []
            for order in currentList:
                if len(deliveriesList) ==0:
                    if firstOrder ==None:
                        firstOrder = order
                    startPoint = copy.deepcopy(environmentService.depot)
                    startPoint.deliveryTimeStart = firstOrder.deliveryTimeStart
                    # travelTime = travellingService.doCalucateTravelNode(firstOrder,environmentService.depot,firstOrder.deliveryTimeStart)
                    delivery1 = Delivery()
                    delivery1.order = startPoint
                    delivery1.deliveryTime = firstOrder.deliveryTimeStart
                    delivery2 = Delivery()
                    delivery2.order = copy.deepcopy(environmentService.depot)


                deliveryObject = Delivery()
                deliveryObject.order = order
                deliveryObject.serviceTime = 600
                checkTempDeliveriesList = copy.deepcopy(deliveriesList)
                checkTempDeliveriesList.append(deliveryObject)
                temp = []
                temp.append([delivery1] + checkTempDeliveriesList + [delivery2])
                print(temp)
                # exit()
                valid, newMutliDeliveriesList = self.checkSingleValidFromTempPath(temp)

                if valid ==True:
                    deliveriesList = checkTempDeliveriesList
                    del sortedStartTimeOrderList[sortedStartTimeOrderList.index(order)]
                    print("sortedStartTimeOrderList",len(sortedStartTimeOrderList))
                    firstOrder =None
                    # timeWindowCount =0
                else:
                    if newMutliDeliveriesList =="FALSE Time Windows 1":
                        print(newMutliDeliveriesList)
                        print(deliveryObject)
                        print(delivery1)
                        exit()
                        # exit()
            timeWindowCount+=1

            currentList = sortedStartTimeOrderList
            totalDriverList.append([delivery1] + deliveriesList + [delivery2])
        return totalDriverList
        # print(totalDriverList)
        #
        #
        # exit()
        pass
nearestNeighborService = NearestNeighborService()
