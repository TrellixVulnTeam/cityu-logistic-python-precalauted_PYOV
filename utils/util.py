
import numpy as np
from datetime import datetime

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from dataset.EdgeDataset import edgeDataset
from dataset.NodeDataset import nodeDataset


def between(d1,d2,d3):
    if d1 <= d2 <= d3:
        return True
    else:
        return False

def stringToDate(date):
    startDate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

def loadDataFromnpz(path):
    print('load numpy', path)
    x = np.load(path,allow_pickle=True)
    for k in x.files:
        print(k)
        return x[k]

def heuristicDistance(a,b):
    (x1, y1) = (float(a.lat),float(a.lng))
    (x2, y2) = (float(b.lat),float(b.lng))
    return abs(x1 - x2) + abs(y1 - y2)
def heuristicDistanceBetweenLatLng(lat1,lng1,lat2,lng2):
    (x1, y1) = (float(lat1),float(lng1))
    (x2, y2) = (float(lat2),float(lng2))
    return abs(x1 - x2) + abs(y1 - y2)



def diffBetweenDateTime(d1,d2):
    duration =  d1 - d2                          # For build-in functions
    duration_in_s = duration.total_seconds()
    return int(duration_in_s)

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

def getNearestNodeByLatLng(lat, lng):
    minDistance = 10000
    currentNode = nodeDataset.nodes[5000]

    for edgeId in edgeDataset.edges:
        edge = edgeDataset.edges[edgeId]

        distance = heuristicDistanceBetweenLatLng(lat,lng,edge.o_node.lat,edge.o_node.lng)
        if distance < minDistance:
            minDistance = distance
            currentNode = edge.o_node
        distance = heuristicDistanceBetweenLatLng(lat,lng,edge.o_node.lat,edge.o_node.lng)
        if distance < minDistance:
            minDistance = distance
            currentNode = edge.d_node
    return currentNode