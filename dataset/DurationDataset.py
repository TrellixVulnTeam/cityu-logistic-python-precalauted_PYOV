import os,sys,inspect

from excpetions.TimeWindowExceeded import TimeWindowExceeded

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from modelObjects.Edge import Edge
from Common import Common
import requests
import json
import numpy as np
import datetime
from utils.util import loadDataFromnpz
from utils.util import between
from dataset.EdgeDataset import edgeDataset
from utils.SingletonMetaclass import SingletonMetaclass

class DurationDataset(metaclass=SingletonMetaclass):
    def __init__(self):
        
        self.loadingDurationData()

    def loadingDurationData(self,):

        path = os.path.join(os.getcwd(), "data/road_duration.npz")
        temp =np.load(path,allow_pickle=True)
        self.durationsNumpy = temp['duration']
        self.timesNumpy = temp['time']
        self.edgesIdNumpy= temp['roadId']
        self.staticDurationsNumpy = self.durationsNumpy[:,0]
        # print(self.timesNumpy)

    def getTimeIndex(self,targetTime):
        newTargetTime = targetTime.replace(2019, 11, 25)
        if targetTime <= self.timesNumpy[0]:
            return 0
        if targetTime >= self.timesNumpy[-1]:
            return len(self.timesNumpy)-1
        for index in range(len(self.timesNumpy)):
            if index == len(self.timesNumpy)-1:
                print("Time-windows condition is Unfulfilled for %s, try to find other solution" %(targetTime))
                raise TimeWindowExceeded

            if between(self.timesNumpy[index], newTargetTime, self.timesNumpy[index+1]):
                return index
    def getEdgeIdIndex(self, edgeId):
        # print(self.edgesIdNumpy.tolist())
        
        found_list = np.where(self.edgesIdNumpy == int(edgeId))[0]
        if len(found_list)==0:
            # raise ValueError('No this Edge {} in the duration record',format(edgeId))
            # print('No this Edge {} in the duration record',format(edgeId))
            return -1
        found_index = found_list[0]
        # print(found_index)
        return found_index

    def getStaticDurationByEdgeIdFromData(self,edgeId,):
        edgeIdIndex = self.getEdgeIdIndex(edgeId)
        if edgeIdIndex ==-1:
            return -1

        value = self.staticDurationsNumpy[edgeIdIndex]

        return int(value)

    def getStaticDurationByEdgeId(self, edgeId):

        edge = edgeDataset.getEdgeById(edgeId)
        return self.getStaticDurationByEdgeIdFromData(edge.v_id)


    def getDynamicDurationByEdgeIdAndTime(self,edgeId, targetTime):

        timelotIndex = self.getTimeIndex(targetTime)

        edgeIdIndex = self.getEdgeIdIndex(edgeId)
        if edgeIdIndex ==-1:
            return -1
        value = self.durationsNumpy[edgeIdIndex][timelotIndex]

        return int(value)

    def getDurationByEdgeIdAndTime(self,edgeId, targetTime):
        edge = edgeDataset.getEdgeById(edgeId)
        value = self.getDynamicDurationByEdgeIdAndTime(edge.v_id, targetTime)

        return value
    

durationDataset = DurationDataset()
print("Duration Dataset initialized")