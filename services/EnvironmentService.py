import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from dataset.DepotDataset import depotDataset
from dataset.NodeDataset import nodeDataset
from dataset.DriverVehicleDataset import driverVehicleDataset
from dataset.OrderDataset import orderDataset
from services.AStarService import aStarService
from Common import Common
import networkx as nx
from modelObjects.Depot import Depot
from modelObjects.Delivery import Delivery
import collections
from utils.SingletonMetaclass import SingletonMetaclass
import copy
class EnvironmentService(metaclass=SingletonMetaclass):
    def __init__(self):
        self.date = Common.deliveryDate
        self.startTimeWindow = Common.startTimeWindow
        self.endTimeWindow = Common.endTimeWindow
        self.depot = depotDataset.depot
        self.orders = orderDataset.orders
        self.driverVehicles = driverVehicleDataset.driverVehicles

    def mutliDeliveriesListToOrderList(self,multiDeliveies):
        routes = []

        for singleDeliveryList in multiDeliveies:
            for index in range(1,len(singleDeliveryList)):
                routes.append(singleDeliveryList[index].order)
            # if type(order) is Depot:
        # print(len(routes))
        # print(routes)
        # exit()
        return routes


    def orderToDelivery(self):
        delivery = Delivery()
        delivery.order
        return delivery


    def orderListToMutliDeliveriesList(self, orderList):
        routes = []
        deliveriesList =[]
        for order in orderList:
            if type(order) is Depot:
                delivery1 = Delivery()
                delivery1.order = order
                delivery2 = Delivery()
                delivery2.order = order
                temp = [delivery1] + deliveriesList + [delivery2]
                routes.append(temp)
                deliveriesList = []
                continue
            deliveryObject = Delivery()
            deliveryObject.order = order
            deliveriesList.append(deliveryObject)
        delivery1 = Delivery()
        delivery1.order = copy.deepcopy(self.depot)
        delivery2 = Delivery()
        delivery2.order = copy.deepcopy(self.depot)
        lastDeliveriesList = [delivery1] + deliveriesList + [delivery2]
        routes.append(lastDeliveriesList)
        # print(routes)
        return routes
    # cap of vehicle
    def constaint1(self, mutliDeliveriesList):
        capacityList = []
        for deliveryRoute in mutliDeliveriesList:
            c = 0.0

            for delivery in deliveryRoute:
                c +=delivery.order.capacity
            capacityList.append(c)

        vehiclesCap = []
        for driverVehicle in self.driverVehicles:
            vehiclesCap.append(driverVehicle.capacity)
        vehiclesCap = sorted(vehiclesCap, reverse=True)
        capacityList = sorted(capacityList, reverse=True)

        # print("len(self.driverVehicles)", len(self.driverVehicles))
        # print("len(mutliDeliveriesList)", len(mutliDeliveriesList))
        if len(mutliDeliveriesList) != len(self.driverVehicles):

            return False
        # print("vehiclesCap",vehiclesCap)
        # print("capacityList", capacityList)
        for i in range(len(capacityList)):
            if vehiclesCap[i] <capacityList[i]:
                return False

        return True

    # num of node
    def constaint2(self,mutliDeliveriesList):
        tempOrderList = []
        for deliveries in mutliDeliveriesList:
            for delivery in deliveries:
                tempOrderList.append(delivery.order)


        # print(len(tempOrderList))

        for order in self.orders:
            temp = next((o for o in tempOrderList if o.orderId == order.orderId), None)
            if temp ==None:
                return False
        # print("len(set(your_list))",len(set(tempOrderList)))
        # if len(set(your_list)) != (len(self.orders) +1):

        duplications = [item for item, count in collections.Counter(tempOrderList).items() if count > 1]
        for dup in duplications:
            if type(dup) != Depot:
                return False
        # print('c2 order, in duplication')
        return True

    # x should be depot 
    # num of vehicle

    def constaint3(self,mutliDeliveriesList):
        if len(mutliDeliveriesList) != len(self.driverVehicles):
            return False
        else:
            return True


    def constaint4(self,mutliDeliveriesList):
        for deliveryList in mutliDeliveriesList:
            lastDelivery = deliveryList[-1]
            # print("lastDelivery", lastDelivery)
            if lastDelivery.deliveryTime > self.endTimeWindow:
                return False
        return True

    def isSingleOrderCapacityVaild(self,signleDelivery):
        capacityList = []
        for deliveryRoute in signleDelivery:
            c = 0.0
            for delivery in deliveryRoute:
                c += delivery.order.capacity
            capacityList.append(c)

        vehiclesCap = []
        for driverVehicle in self.driverVehicles:
            vehiclesCap.append(driverVehicle.capacity)

        vehiclesCap = sorted(vehiclesCap, reverse=True)
        capacityList = sorted(capacityList, reverse=True)
        if vehiclesCap[0] < capacityList[0]:
            return False
        else:
            return True

    def isOrderStructureValid(self,mutliDeliveriesList):
        
        return self.constaint1(mutliDeliveriesList) and self.constaint2(mutliDeliveriesList) and self.constaint3(mutliDeliveriesList)
    
    def isTimeWindowsVaild(self,mutliDeliveriesList):
        return self.constaint4(mutliDeliveriesList)

environmentService = EnvironmentService()
