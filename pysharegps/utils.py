#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2012 Jonathan Delvaux <pytries@djoproject.net>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.

#http://www.movable-type.co.uk/scripts/latlong.html

#TODO add more functionnalitites from the website
    #not prioritary
    #make a special line object, see the description in the middle of sharegps.py


from math import *
import sys

R = 6371.000

def getCoordString(point):
    return str(point.lat)+", "+str(point.lon)

def parseCoordString(string):
    string = string.strip()
    string_token = string.split(",")
    
    nonEmptyToken = []
    
    for token in string_token:
        token = token.strip()
        if len(token) == 0:
            continue
            
        nonEmptyToken.append(token)
        
    if len(nonEmptyToken) != 2:
        raise ValueError("Coordinate parse string : invalid format, expected \"0.0, 0.0\", got \""+str(string)+"\"")
    
    lat = 0.0
    try:
        lat = float(nonEmptyToken[0])
    except ValueError as ve:
        raise ValueError("Coordinate parse string : invalid latitude format, "+str(ve))
    
    if lat < -90.0 or lat > 90.0:
        raise ValueError("Coordinate parse string : invalid latitude value, expected a value between -90.0 and 90.0, got "+str(lat))
        
    lon = 0.0
    try:
        lon = float(nonEmptyToken[1])
    except ValueError as ve:
        raise ValueError("Coordinate parse string : invalid longitude, "+str(ve))
        
    if lon < -180.0 or lon > 180.0:
        raise ValueError("Coordinate parse string : invalid longitude value, expected a value between -180.0 and 180.0, got "+str(lon))
        
    return gpsPoint(lat,lon)

def getDistance(pointA, pointB):
    dLat = radians( (pointB.lat-pointA.lat) )
    dLon = radians( (pointB.lon-pointA.lon) )
    lat1 = radians( pointA.lat )
    lat2 = radians( pointB.lat )

    a = sin(dLat/2.0) * sin(dLat/2.0) + sin(dLon/2.0) * sin(dLon/2.0) * cos(lat1) * cos(lat2); 
    c = 2.0 * atan2(sqrt(a), sqrt(1.0-a)); 
    d = R * c;
    
    return abs(d)

class gpsPoint(object):
    def __init__(self,lat = 0.0,lon = 0.0, name = "", descr = None):
        self.lat = lat
        self.lon = lon
        self.name = name
        self.descr = descr

class gpsSimpleLine(object):
    def __init__(self, start, end, descr = None)
        self.start = start
        self.end = end
        self.descr = descr

class gpsLine(List):
    #TODO catch list update event
        #to set the variable self.lengthComputed to False

    def __init__(self):
        self.lengthComputed = False
        self.length = None

    def isLengthComputed(self)
        return self.lengthComputed

    def getLength(self):
        return self.length

    def computeLength(self):
        pass #TODO


def getBearing(pointA, pointB)#(pointALat,pointALon, pointBLat, pointBLon):
    dLat = radians( (pointB.lat-pointA.lat) )
    dLon = radians( (pointB.lon-pointA.lon) )
    lat1 = radians( pointA.lat )
    lat2 = radians( pointB.lat )

    y = sin(dLon) * cos(lat2);
    x = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(dLon);

    return degrees ( atan2(y, x) )
    
def getLineDistance(point, linePointA, linePointB) #(pointXLat,pointXLon,linePointALat,linePointALon,linePointBLat,linePointBLon):
    
    d13 = getDistance(linePointA,point)
    brng13 = radians( getBearing(linePointA,point) )
    brng12 = radians( getBearing(linePointA,linePointB) )
    
    return abs(asin(sin(d13/R)*sin(brng13-brng12)) * R);


#def sortDistance(x,y):
#    disX,ditType,nameX = x
#    disY,ditType,nameY = y
#    
#    return int(disX-disY)




class nearestGpsPoint(gpsPoint):
    def __init__(self, lat = 0.0,lon = 0.0, distance = 0.0, name = "", descr = None, fromPoint = None)
        gpsPoint.__init__(lat, lon, descr)
        self.distance = distance
        self.fromPoint = fromPoint

def findTheNearestPoint(pointX, pointList):
    if len(pointList) == 0:
        return None

    nearest = (sys.maxint,None, None)
    
    for k, point in pointList.iteritems():
        distance = getDistance(pointX, point)

        if distance < nearest[0]:
            nearest = (distance,k, point)
    
    return nearestGpsPoint(nearest[2].lat, nearest[2].lon, nearest[0], k, nearest[2].descr, nearest[1], pointX)

DISTANCEFROMLINE       = "from line"
DISTANCEFROMSTARTPOINT = "from starting point"
DISTANCEFROMENDPOINT   = "from end point"

class nearestGpsLine(gpsSimpleLine):
    def __init__(self, start, end, distance = 0.0, distFrom = DISTANCEFROMLINE, descr = None, fromPoint = None)
        gpsSimpleLine.__init__(start, end, descr)
        self.distance = distance
        self.distFrom = distFrom
        self.fromPoint = fromPoint

def findThenearestLine(pointX, lineList):
    if len(lineList) == 0:
        return None

    nearest = (sys.maxint,DISTANCEFROMLINE,None, None)
    for k, line in lineList.iteritems():
        distanceFromStartPoint = getDistance(pointX,line.start)
        distanceFromEndPoint   = getDistance(pointX,line.end)
        distanceFromTheLine    = getLineDistance(pointX,line.start,line.end )
        segmentLength          = getDistance(line.start,line.end)
        
        #print "    distanceFromTheLine="+str(distanceFromTheLine)
            
        if sqrt( distanceFromStartPoint**2 - distanceFromTheLine**2 ) > segmentLength or sqrt( distanceFromEndPoint**2 - distanceFromTheLine**2 ) > segmentLength:
            #not on the segment
            
            #on prend la plus petite distance par rapport aux gares
            if distanceFromStartPoint < distanceFromEndPoint:
                distance = distanceFromStartPoint
                distanceType = DISTANCEFROMSTARTPOINT
            else:
                distance = distanceFromEndPoint
                distanceType = DISTANCEFROMENDPOINT
        else:#on the segment 
            
            #on prend la distance a partir de la ligne
            distance = distanceFromTheLine
            distanceType = DISTANCEFROMLINE
    
        if distance < nearest[0]:
            nearest = (distance,distanceType,k,line)
    
    return nearestGpsLine(nearest[3].start, nearest[3].end, nearest[0], nearest[1],nearest[2],pointX)



