
# coding: utf-8

# In[1]:


class Delivery:
    def __init__(self,):
        self.driverVehicle=None
        self.order = None
        self.deliveryDate=None
        self.deliveryTime=None
        self.aStarNodeList = None
        self.serviceTime=float(600)

    def __repr__(self):
        # return "order : {} ,deliveryTime : {} , serviceTime: {}".format(self.order,self.deliveryTime,self.serviceTime)
        return "order : {} ,deliveryTime : {}, time window :{} - {}".format(self.order, self.deliveryTime,self.order.deliveryTimeStart, self.order.deliveryTimeEnd)


