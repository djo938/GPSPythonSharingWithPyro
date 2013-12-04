#!/usr/bin/python

#http://www.movable-type.co.uk/scripts/latlong.html

from math import *
import sys

R = 6371.000

def getDistance(pointALat,pointALon, pointBLat, pointBLon):
    dLat = radians( (pointBLat-pointALat) )
    dLon = radians( (pointBLon-pointALon) )
    lat1 = radians( pointALat )
    lat2 = radians( pointBLat )

    a = sin(dLat/2.0) * sin(dLat/2.0) + sin(dLon/2.0) * sin(dLon/2.0) * cos(lat1) * cos(lat2); 
    c = 2.0 * atan2(sqrt(a), sqrt(1.0-a)); 
    d = R * c;
    
    return d

class gpsPoint(object):
    def __init__(self,latitude,longitude):
        self.latitude = latitude
        self.longitude = longitude
        
class gpsLine(object):
    def __init__(self,startPoint,endPoint,name=None):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.name = name
        
        self.segmentLength = getDistance(startPoint.latitude,startPoint.longitude,endPoint.latitude,endPoint.longitude)
        
        
def getBearing(pointALat,pointALon, pointBLat, pointBLon):
    dLat = radians( (pointBLat-pointALat) )
    dLon = radians( (pointBLon-pointALon) )
    lat1 = radians( pointALat )
    lat2 = radians( pointBLat )

    y = sin(dLon) * cos(lat2);
    x = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(dLon);

    return degrees ( atan2(y, x) )
    
def getLineDistance(pointXLat,pointXLon,linePointALat,linePointALon,linePointBLat,linePointBLon):
    
    d13 = getDistance(linePointALat,linePointALon,pointXLat,pointXLon)
    brng13 = radians( getBearing(linePointALat,linePointALon,pointXLat,pointXLon) )
    brng12 = radians( getBearing(linePointALat,linePointALon,linePointBLat,linePointBLon) )
    
    return asin(sin(d13/R)*sin(brng13-brng12)) * R;

def sortDistance(x,y):
    disX,ditType,nameX = x
    disY,ditType,nameY = y
    
    return int(disX-disY)

DISTANCEFROMLINE = "from line"
DISTANCEFROMSTARTPOINT = "from starting point"
DISTANCEFROMENDPOINT = "from end point"

def findThenearestLine(pointXLat,pointXLon, lineList):
    nearest = (sys.maxint,DISTANCEFROMLINE,"the farest")
    for line in lineList:
        #print line.name
        
        distanceFromStartPoint = getDistance(pointXLat,pointXLon,line.startPoint.latitude,line.startPoint.longitude)
        distanceFromEndPoint = getDistance(pointXLat,pointXLon,line.endPoint.latitude,line.endPoint.longitude)
        
        #print "    distanceFromStartPoint="+str(distanceFromStartPoint)
        #print "    distanceFromEndPoint="+str(distanceFromEndPoint)
        #print "    segmentLength="+str(line.segmentLength)
        
        distanceFromTheLine = getLineDistance(pointXLat,pointXLon,line.startPoint.latitude,line.startPoint.longitude,line.endPoint.latitude,line.endPoint.longitude )
        
        #print "    distanceFromTheLine="+str(distanceFromTheLine)
        
        if distanceFromTheLine < 0.0:
            distanceFromTheLine *= -1
            
        if sqrt( distanceFromStartPoint**2 - distanceFromTheLine**2 ) > line.segmentLength or sqrt( distanceFromEndPoint**2 - distanceFromTheLine**2 ) > line.segmentLength:
            #print "    not on the segment"
            
            #on prend la plus petite distance par rapport aux gares
            if distanceFromStartPoint < distanceFromEndPoint:
                distance = distanceFromStartPoint
                distanceType = DISTANCEFROMSTARTPOINT
            else:
                distance = distanceFromEndPoint
                distanceType = DISTANCEFROMENDPOINT
        else:
            #print "    on the segment"    
            
            #on prend la distance a partir de la ligne
            distance = distanceFromTheLine
            distanceType = DISTANCEFROMLINE
    
        if distance < nearest[0]:
            nearest = (distance,distanceType,line.name)
    
    return nearest



