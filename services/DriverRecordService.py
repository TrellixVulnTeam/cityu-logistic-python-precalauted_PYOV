
import os, sys, inspect


from dataset.DepotDataset import depotDataset
from modelObjects.FitnessObject import FitnessObject
from services.EnvironmentService import environmentService
from services.TravellingService import travellingService

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from dataset.DriverRecordDataset import driverRecordDataset
from dataset.DurationDataset import durationDataset
import random
from utils.SingletonMetaclass import SingletonMetaclass
import datetime
import numpy as np


class DriverRecordService(metaclass=SingletonMetaclass):
    def __init__(self, ):
        pass

    def checkDriverRecord(self,num):
        path = "data/driverRecord/order%sv.csv"%num
        driverRecordDataset.loadingData(path)
        driverRecords = driverRecordDataset.driverRecords
        orderSet = []
        for key in driverRecords:
            driverDeliveryOrder = driverRecords[key]
            for order in driverDeliveryOrder:
                orderSet.append(order)
            orderSet.append(depotDataset.depot)

        deliveriesList = environmentService.orderListToMutliDeliveriesList(orderSet)
        newMutliDeliveriesList = []
        print(len(deliveriesList))
        for singleDelivery in deliveriesList:
            newMutliDeliveriesList.append(travellingService.calucateTravelNodeFromDeliveryListWithOutWindowLimit(singleDelivery,
                                                                                               singleDelivery[
                                                                                                   0].order.deliveryTimeStart,
                                                                                               singleDelivery[
                                                                                                   -1].order.deliveryTimeEnd))
        fitnessObject = FitnessObject(deliveriesList, newMutliDeliveriesList)
        fitnessObject.routeFitness()

        nCsv = open('./result/%s_o.txt' % (num), 'a+', encoding='utf-8-sig')
        nCsv.write("Total vehicle: %s\n" % fitnessObject.vehicleNum)
        nCsv.write("TotalDuration: %ss\n" % fitnessObject.totalDuration)
        nCsv.write(
            "TotalTravelDuration: %ss\n" % (fitnessObject.totalDurationWithoutNonUseVehicle - fitnessObject.totalServiceTime))

        return fitnessObject
        # vehicleCount = 0
        # totalService= 0
        # for vehicleIndex in range(len(newMutliDeliveriesList)):
        #     # print("Vehicle %s:" %(vehicleIndex+1))
        #     if len(newMutliDeliveriesList[vehicleIndex]) > 2:
        #         vehicleCount += 1
        #         for delivery in newMutliDeliveriesList[vehicleIndex]:
        #             totalService += delivery.serviceTime

                # print(fitnessResult.multiDeliveriesList[vehicleIndex])

        # print(fitnessObject.totalDuration)
        # print("vehicleCount", vehicleCount)
        # print("totalService",totalService)
        # pass

driverRecordService = DriverRecordService()
