
# coding: utf-8

# In[1]:


class DriverVehicle:
    def __init__(self,):
        self.driverId=None
        self.userId = None
        self.firstName=None
        self.lastName=None
        self.phoneNumber=None
        self.vehicleId=None
        self.vehicleCode=None
        self.capacity=None
        self.deliveryDate=None

    def __repr__(self):
        return "driverId :%s , vehicleId: %s " %(self.driverId,self.vehicleId)
