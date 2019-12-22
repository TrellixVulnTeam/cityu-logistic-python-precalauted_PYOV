
# coding: utf-8

# In[ ]:

import numpy as np

import datetime
import math
from Common import Common
from utils.util import diffBetweenDateTime

class FitnessObject:
    def __init__(self, fullPath, multiDeliveriesList):
        self.multiDeliveriesList = multiDeliveriesList
        self.fullPath = fullPath
        self.totalDuration = 0
        self.totalDurationWithoutNonUseVehicle = 0
        self.vehicleNum = 0
        self.fitnessValue= 0.0
        self.totalServiceTime = 0
    
    def routeFitness(self):
        totalDuration = 0
        totalDurationWithoutNonUseVehicle = 0
        vehicleNum = 0
        serviceTime = 0
        for deliveriesList in self.multiDeliveriesList:
            if len(deliveriesList) >2:
                for delivery in deliveriesList:
                    serviceTime += delivery.serviceTime
                vehicleNum +=1
                endDelivery = deliveriesList[-1]
                endDeliveryTime = endDelivery.deliveryTime
                totalDurationWithoutNonUseVehicle += diffBetweenDateTime(endDeliveryTime,deliveriesList[0].deliveryTime)
            endDelivery = deliveriesList[-1]
            endDeliveryTime = endDelivery.deliveryTime
            totalDuration += diffBetweenDateTime(endDeliveryTime, deliveriesList[0].deliveryTime)


        self.totalServiceTime = serviceTime
        self.vehicleNum = vehicleNum
        self.totalDurationWithoutNonUseVehicle = totalDurationWithoutNonUseVehicle
        self.totalDuration = totalDuration
        self.fitnessValue = 3600 / totalDuration # 1 hour: 3600 seconds
        return self.fitnessValue
    def __repr__(self):
        return str(self.totalDuration)
