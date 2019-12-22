import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from modelObjects.DriverVehicle import DriverVehicle
from Common import Common
import requests
import json
from utils.SingletonMetaclass import SingletonMetaclass
import datetime

class DriverVehicleDataset(metaclass=SingletonMetaclass):
    def __init__(self):
        self.driverVehicles = []

    def loadingData(self,):
        for index in range(6):
            driverVehicle = DriverVehicle()
            driverVehicle.driverId = index
            driverVehicle.userId = index
            driverVehicle.firstName = index
            driverVehicle.lastName = index
            driverVehicle.phoneNumber = index
            driverVehicle.vehicleId = index
            driverVehicle.vehicleCode = index
            driverVehicle.capacity = 3000
            self.driverVehicles.append(driverVehicle)

    def getDriverVehicleByVIdandDId(self,vId,dId):
        return next((x for x in self.driverVehicles if x.driverId == dId and  x.vehicleId == vId), None)

driverVehicleDataset = DriverVehicleDataset()
print("DriverVehicle Dataset initialized")