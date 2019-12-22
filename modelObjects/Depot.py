
# coding: utf-8

# In[1]:
from modelObjects.Order import Order

class Depot(Order):
    def __init__(self):
        self.orderId = 0
        self.lat = None
        self.lng = None
        self.address = None
