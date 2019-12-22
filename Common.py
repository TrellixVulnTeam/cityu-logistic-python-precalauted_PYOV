import datetime

from utils.SingletonMetaclass import SingletonMetaclass


class Common(metaclass=SingletonMetaclass):
    
    def __init__(self):
        self.serverPath = 'http://104.197.155.67/'
        # self.apiPath = 'http://localhost:8888/index.php/'
        self.apiPath = "https://deep-rec.com/logistic/index.php/"
        self.deliveryDate = None
        self.startTimeWindow = None
        self.endTimeWindow = None
        self.thread = 1
        self.len_population = 1000
        self.crossRate = 0.2
        self.mutationRate = 0.04
        self.max_generations = 200
        self.len_max_keep = 20

Common = Common()

