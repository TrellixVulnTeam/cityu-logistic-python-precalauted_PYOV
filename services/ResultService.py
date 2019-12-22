import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from dataset.DriverVehicleDataset import driverVehicleDataset

from Common import Common
import requests
import json
from utils.SingletonMetaclass import SingletonMetaclass
from utils.util import myconverter
from utils.util import diffBetweenDateTime


class ResultService(metaclass=SingletonMetaclass):
    def __init__(self):
        pass
    def sendResultToDB(self, finessResult):
        data = []
        multiDeliveriesList = finessResult.multiDeliveriesList
        driverVehicleCount = 0

        for deliveryList in multiDeliveriesList:
            oneVehicleDelivery = []
            if len(deliveryList) ==2:
                continue
            for i in range(len(deliveryList)):
                delivery = deliveryList[i]

                jsonDelivery = {}
                jsonDelivery["orderId"] = delivery.order.orderId
                jsonDelivery["deliveryTime"] = delivery.deliveryTime
                jsonDelivery["serviceTime"] = delivery.serviceTime
                jsonDelivery["routes"] = []
                jsonDelivery["driverId"] = driverVehicleDataset.driverVehicles[driverVehicleCount].driverId
                jsonDelivery["vehicleId"] = driverVehicleDataset.driverVehicles[driverVehicleCount].vehicleId
                travellingTime = 0
                if i!=0:
                    previousDelivery = deliveryList[i-1]
                    travellingTime = diffBetweenDateTime(delivery.deliveryTime,previousDelivery.deliveryTime) - previousDelivery.serviceTime
                jsonDelivery["travellingTime"] =travellingTime
                if delivery.aStarNodeList != None:
                    for aStarNode in delivery.aStarNodeList:
                        jsonAStarNode = {}
                        jsonAStarNode["nodeId"] = aStarNode.node.nodeId
                        jsonDelivery["routes"].append(jsonAStarNode)
                        
                jsonData = json.dumps(jsonDelivery,default = myconverter)
                # print("-----------")
                # print(jsonData)
                r = requests.post(Common.apiPath +"deliveries/storeDeliveries", json=jsonData)
                print(r.text)
            driverVehicleCount+=1

    def sendDynamicResultToDB(self, dynamicFinessResult):
        dynamicDriverList = dynamicFinessResult.dynamicDriverList

        for dynamicDriver in dynamicDriverList:
            # print(dynamicDriver.remainDeliveries)
            if len(dynamicDriver.remainDeliveries) == 2:
                continue
            remainDeliveries = dynamicDriver.remainDeliveries
            for i in range(len(remainDeliveries)):
                delivery = remainDeliveries[i]
                jsonDelivery = {}
                jsonDelivery["orderId"] = delivery.order.orderId
                if delivery.order.orderId == -1:
                    jsonDelivery['startLat'] = dynamicDriver.vehicleLocation.lat
                    jsonDelivery['startLng'] = dynamicDriver.vehicleLocation.lng

                jsonDelivery["deliveryTime"] = delivery.deliveryTime
                jsonDelivery["serviceTime"] = delivery.serviceTime
                jsonDelivery["routes"] = []
                jsonDelivery["driverId"] = dynamicDriver.driverVehicle.driverId
                jsonDelivery["vehicleId"] = dynamicDriver.driverVehicle.vehicleId
                travellingTime = 0

                if i != 0:
                    previousDelivery = remainDeliveries[i - 1]
                    travellingTime = diffBetweenDateTime(delivery.deliveryTime,
                                                         previousDelivery.deliveryTime) - previousDelivery.serviceTime
                jsonDelivery["travellingTime"] = travellingTime
                if delivery.aStarNodeList != None:
                    for aStarNode in delivery.aStarNodeList:
                        jsonAStarNode = {}
                        jsonAStarNode["nodeId"] = aStarNode.node.nodeId
                        jsonDelivery["routes"].append(jsonAStarNode)

                jsonData = json.dumps(jsonDelivery, default=myconverter)
                # print("-----------")
                # print(jsonData)
                r = requests.post(Common.apiPath + "deliveries/updateDynamicDeliveries", json=jsonData)
                print(r.text)

        

resultService = ResultService()
