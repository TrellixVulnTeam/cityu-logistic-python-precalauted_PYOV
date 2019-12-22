
# coding: utf-8

# In[1]:


class Order:
    def __init__(self):
        self.orderId=None
        self.areaId = None
        self.invoiceNo=None
        self.invoiceCode=None
        self.company=None
        self.deliveryDate=None
        self.clientName=None
        self.clientPhone1=None
        self.clientPhone2=None
        self.address=None
        self.lat=None
        self.lng=None
        self.productName=None
        self.productNumber = None
        self.capacity=0
        self.charge=None
        self.remark=None
        self.categoryId=None
        self.statusId=None
        self.deliveryTimeStart=None
        self.deliveryTimeEnd=None
    


    def setNearestNode(self,node):
        self.nearestNode = node

    def getNearestNode(self):
        return self.nearestNode

    def __repr__(self):
        # return "orderId : {}".format(self.orderId)
        return "Id: {}, nodeId : {}".format(self.orderId, self.nearestNode.nodeId)


