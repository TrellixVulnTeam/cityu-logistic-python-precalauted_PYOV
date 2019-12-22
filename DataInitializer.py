import os,sys,inspect

from dataset.DepotDataset import depotDataset
from dataset.PreComputedDataset import preComputedDataset

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from dataset.DriverVehicleDataset import driverVehicleDataset
from dataset.OrderDataset import orderDataset

from utils.SingletonMetaclass import SingletonMetaclass
from Common import Common


class DataInitializer(metaclass=SingletonMetaclass):
    def __init__(self):
        pass
    def setStartDate(self,targetDate):
        Common.deliveryDate = targetDate.date()
        Common.startTimeWindow = targetDate

    def setTimeEndWindows(self,endTimeWindows):
        Common.endTimeWindow = endTimeWindows
    def dynamicPickupGenerate(self):
       driverVehicleDataset.loadingData()
       orderDataset.loadDynamicOrder(Common.deliveryDate)
       depotDataset.loadingData()

    def normalGenerate(self,orderIndex):

       driverVehicleDataset.loadingData()
       path = 'data/order%s.csv' %(orderIndex)
       orderDataset.loadingData(Common.deliveryDate,path)
       depotDataset.loadingData()
       preComputedDataset.loadingPreComputedData(orderIndex)


dataInitializer = DataInitializer()
