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

class PreComputedDataset(metaclass=SingletonMetaclass):
    def __init__(self):
        pass


    def loadingPreComputedData(self,num):
        path = os.path.join(os.getcwd(), "data/%s.npz" %num)
        temp =np.load(path,allow_pickle=True)
        self.durationsNumpy = temp['duration']
        self.timesNumpy = temp['time']
        self.edgesIdNumpy= temp['nodeId']
        self.staticDurationsNumpy = self.durationsNumpy[:,0]
        print(self.durationsNumpy.shape)
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

    def getNodeIndex(self, nodeId):
        # print(self.edgesIdNumpy.tolist())
        
        found_list = np.where(self.edgesIdNumpy == int(nodeId))[0]
        if len(found_list)==0:
            print('No this Node {} in the precomputed record',format(nodeId))
            raise ValueError('No this Node {} in the precomputed record',format(nodeId))

            return -1
        found_index = found_list[0]
        # print(found_index)
        return found_index

    def getStaticDurationByEdgeId(self, edgeId):

        edge = edgeDataset.getEdgeById(edgeId)
        return self.getStaticDurationByEdgeIdFromData(edge.v_id)


    def getDynamicDurationByNodeIdsAndTime(self,nodeId1,nodeId2, targetTime):

        timelotIndex = self.getTimeIndex(targetTime)

        nodeIdIndex1 = self.getNodeIndex(nodeId1)
        nodeIdIndex2 = self.getNodeIndex(nodeId2)

        # if nodeIdIndex ==-1:
        #     return -1
        value = self.durationsNumpy[timelotIndex][nodeIdIndex1][nodeIdIndex2]
        # print("from Node %s to Node %s, value %s, time %s" %(nodeId1,nodeId2,value,targetTime))

        return int(value)

    def getDurationByNodeIdAndTime(self,nodeId1,nodeId2, targetTime):
        # edge = edgeDataset.getEdgeById(edgeId)
        value = self.getDynamicDurationByNodeIdsAndTime(nodeId1,nodeId2, targetTime)

        return value

preComputedDataset = PreComputedDataset()
print("preComputed Dataset  initialized")