
import numpy as np
from datetime import datetime
from datetime import timedelta
import traceback
class DataController:
    
    def __init__(self):
        self.durations = np.array([])
        self.times = np.array([])
        self.road_ids = np.array([])
        
    def loadMultiDuration(self, count):
        targetDuration = np.array([])
        for i in range(count):
            fileName = "data/training_duration_{}.npz".format(i)
            if targetDuration.size ==0:
                targetDuration = self.loadDataFromnpz(fileName)[:,self.start_index:self.end_index]
            else:
                temp = self.loadDataFromnpz(fileName)[:,self.start_index:self.end_index]
                targetDuration = np.concatenate((targetDuration,temp), axis=0)
        return targetDuration

    def getTimeRangeIndex(self,startDate,endDate):
        start_index = -1
        end_index =0
        for i in range(len(self.times)):
            target = self.times[i]
            if self.between(startDate,target,endDate):
                if start_index== -1:
                    start_index = i
                end_index = i
        return start_index,end_index
    def getDataFromTimeRange(self, start,end):
        path = "data/training_timelot.npz"
        self.times = self.loadDataFromnpz(path)
        startDate = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        endDate = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        self.start_index,self.end_index = self.getTimeRangeIndex(startDate,endDate)
        print(self.start_index,self.end_index)
        targetDuration = self.loadMultiDuration(9)
        return targetDuration
    def loadDataFromnpz(self, path):
        print('load numpy', path)
        x = np.load(path)
        for k in x.files:
            print(k)
            return x[k]

    def between(self,d1,d2,d3):
        if d1 <= d2 <= d3:
            return True
        else:
            return False

   
dataController = DataController()
date_range = [['2018-11-05 00:00:00','2018-11-05 00:02:00']]
                                                                                                                                                 
for i in date_range:
    name = "data/{}_static".format(i[0][:10])
    dayDuration = dataController.getDataFromTimeRange(i[0],i[1])
    print(dayDuration.shape)
    np.savez_compressed(name,x=dayDuration, timeRange=dataController.times[dataController.start_index:dataController.end_index])



