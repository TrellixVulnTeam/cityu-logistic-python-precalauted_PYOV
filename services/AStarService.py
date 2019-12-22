import os,sys,inspect

from utils.util import diffBetweenDateTime

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from dataset.DurationDataset import durationDataset
from dataset.EdgeDataset import edgeDataset
import networkx as nx
from modelObjects.Node import Node
from services.GraphService import graphService
import datetime
from modelObjects.AStarNode import AStarNode 
from utils.SingletonMetaclass import SingletonMetaclass
from Common import Common
# from services.CPDService import cPDService
class AStarService(metaclass=SingletonMetaclass):

    def __init__(self,):
        print('AStarService Init')
        self.caches = {}


    def calucateAStarValueFromDeliveriesList(self,mutliDeliveriesList):

        for deliveriesList in mutliDeliveriesList:
            if len(deliveriesList) ==2:
                deliveriesList[0].deliveryTime = Common.startTimeWindow
                deliveriesList[1].deliveryTime = Common.startTimeWindow
                continue
            for index in range(len(deliveriesList)-1):
                startDelivery = deliveriesList[index]
                if index ==0:
                    startDelivery.deliveryTime = Common.startTimeWindow

                endDelivery = deliveriesList[index+1]
                fromNode = startDelivery.order.nearestNode
                toNode = endDelivery.order.nearestNode
                if nx.has_path(graphService.G,fromNode.nodeId,toNode.nodeId)==False:
                    print('No path {}, {}'.format(fromNode,toNode))
                else:
                    aStarNodeList = self.doSearch(startDelivery.order.nearestNode,endDelivery.order.nearestNode,startDelivery.deliveryTime + datetime.timedelta(seconds=startDelivery.serviceTime))

                    # aStarNodeList = cPDService.doSearch(startDelivery.order.nearestNode,endDelivery.order.nearestNode,startDelivery.deliveryTime + datetime.timedelta(seconds=startDelivery.serviceTime))

                endDelivery.aStarNodeList = aStarNodeList
                lastAStarNodeDeliveryTime = aStarNodeList[-1].timeSlot
                endDelivery.deliveryTime = lastAStarNodeDeliveryTime
                print('Done', index)
        return mutliDeliveriesList

    def children(self,aStarNode,targetTime):
        childrenEdgeList = edgeDataset.getNodesByStartPoint(aStarNode.node.nodeId)
        childrenAStarNodeList = []
        for endPoint in childrenEdgeList:
            edge = childrenEdgeList[endPoint]
            endNode = Node(endPoint,str(edge.d_lat),str(edge.d_lng))

            value = durationDataset.getDurationByEdgeIdAndTime(edge.v_id,targetTime)
            # print('edge',edge.v_id)
            # print('Value',value)
            aStarNode = AStarNode(value,endNode)

            newTime = targetTime + datetime.timedelta(seconds=value)
            aStarNode.timeSlot = newTime
            childrenAStarNodeList.append(aStarNode)
        return childrenAStarNodeList

    def manhattan(self,startNode,endNode):
        source = startNode.node.nodeId
        target = endNode.node.nodeId
        if nx.has_path(graphService.G,source,target)==False:
            return 3600
        return float(nx.astar_path_length(graphService.G, source,target))
        

    def isAStarNodeEqual(self,a1,a2):
        if str(a1.node.nodeId) == str(a2.node.nodeId):
            return True
        else:
            return False

    def addEdgeIdToAStarNodeList(self,aStarNodeList):
        for index in range(len(aStarNodeList)-1):
            aStarNode  = aStarNodeList[index]
            nextAStarNode = aStarNodeList[index+1]
            edge = edgeDataset.getEdgeByStartPointAndEndPoint(aStarNode.node.nodeId,nextAStarNode.node.nodeId)
            nextAStarNode.edge = edge
            nextAStarNode.edgeId = edge.v_id
        return aStarNodeList

    def nodeListToAStarList(self, nodeList, startTime):
        aStarNodeList = []
        startAStarNode = AStarNode(0,nodeList[0])
        startAStarNode.timeSlot = startTime
        aStarNodeList.append(aStarNodeList)

        for index in range(len(nodeList)-1):
            lastAStarNode = aStarNodeList[-1]
            startNode = nodeList[index]
            nextNode = nodeList[index+1]
            edge = edgeDataset.getEdgeByStartPointAndEndPoint(startNode.lat,nextNode.lng)
            value = durationDataset.getDurationByEdgeIdAndTime(edge.v_id,lastAStarNode.timeSlot)
            aStarNode = AStarNode(value,nextNode)
            newTime = lastAStarNode.timeSlot + datetime.timedelta(seconds=value)
            aStarNode.timeSlot = newTime
            aStarNodeList.append(aStarNode)

    def doSearch(self, startNode, endNode, targetTime):
         #The open and closed sets
        key = "%s-%s-%s"%(targetTime,startNode,endNode)
        if key in self.caches:
            # print("A* cache :%s"%(key))
            return self.caches[key], None

        openset = set()
        closedset = set()
        #Current point is the starting point
        start = AStarNode(0,startNode)
        start.timeSlot = targetTime
        goal = AStarNode(0,endNode)
        current = start

        #Add the starting point to the open set
        openset.add(current)

        while openset:
            #Find the item in the open set with the lowest G + H score
            current = min(openset, key=lambda o:o.G + o.H)
            if self.isAStarNodeEqual(current,goal):
                path = []
                while current.parent:
                    path.append(current)
                    current = current.parent
                path.append(current)
                newList = self.addEdgeIdToAStarNodeList(path[::-1])

                totalTime = 0
                if len(newList)>1:
                    firstNode = newList[0]
                    lastNode = newList[-1]
                    totalTime = diffBetweenDateTime(lastNode.timeSlot,firstNode.timeSlot )
                self.caches[key] = newList
                return newList,totalTime
            openset.remove(current)
            closedset.add(current)

            for aStarNode in self.children(current,current.timeSlot):
                if any(temp.node.nodeId == aStarNode.node.nodeId for temp in closedset):
                    continue
                openedNode = next((temp for temp in openset if temp.node.nodeId == aStarNode.node.nodeId), None)

                if openedNode is not None:
                    new_g = current.G + aStarNode.value
                    if openedNode.G > new_g:
                        #If so, update the node to have a new parent
                        # print(openedNode)
                        openedNode.G = new_g
                        openedNode.parent = current
                        openedNode.timeSlot = aStarNode.timeSlot
                        openedNode.value = aStarNode.value
                        
                else:
                    #If it isn't in the open set, calculate the G and H score for the node
                    aStarNode.G = current.G + aStarNode.value
                    aStarNode.H = self.manhattan(aStarNode, goal)
                    #Set the parent to our current item
                    aStarNode.parent = current
                    
                    #Add it to the set
                    openset.add(aStarNode)
    
        raise ValueError('No Path Found')

aStarService = AStarService()