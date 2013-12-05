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

from math import *
import sys

R = 6371.000

def getCoordString(lat, lon):
    return str(lat)+", "+str(lon)

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
        
    return lat,lon

def getDistance(pointALat,pointALon, pointBLat, pointBLon):
    dLat = radians( (pointBLat-pointALat) )
    dLon = radians( (pointBLon-pointALon) )
    lat1 = radians( pointALat )
    lat2 = radians( pointBLat )

    a = sin(dLat/2.0) * sin(dLat/2.0) + sin(dLon/2.0) * sin(dLon/2.0) * cos(lat1) * cos(lat2); 
    c = 2.0 * atan2(sqrt(a), sqrt(1.0-a)); 
    d = R * c;
    
    return abs(d)

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
    
    return abs(asin(sin(d13/R)*sin(brng13-brng12)) * R);

def sortDistance(x,y):
    disX,ditType,nameX = x
    disY,ditType,nameY = y
    
    return int(disX-disY)

DISTANCEFROMLINE       = "from line"
DISTANCEFROMSTARTPOINT = "from starting point"
DISTANCEFROMENDPOINT   = "from end point"
DISTANCEFROMPOINT      = "from point"

def findTheNearestPoint(pointXLat,pointXLon, pointList):
    nearest = (sys.maxint,DISTANCEFROMPOINT,"no point available", 0.0, 0.0)
    
    for k, point in pointList.iteritems():
        distance = getDistance(pointXLat,pointXLon, point[0], point[1])

        if distance < nearest[0]:
            nearest = (distance,DISTANCEFROMPOINT,k, point[0], point[1])

    return nearest

def findThenearestLine(pointXLat,pointXLon, lineList):
    nearest = (sys.maxint,DISTANCEFROMLINE,"no line available", 0.0, 0.0, 0.0, 0.0)
    for k, line in lineList.iteritems():
        distanceFromStartPoint = getDistance(pointXLat,pointXLon,line[0],line[1])
        distanceFromEndPoint   = getDistance(pointXLat,pointXLon,line[2],line[3])
        distanceFromTheLine    = getLineDistance(pointXLat,pointXLon,line[0],line[1],line[2],line[3] )
        segmentLength          = getDistance(line[0],line[1],line[2],line[3])
        
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
            nearest = (distance,distanceType,k, line[0],line[1],line[2],line[3])
    
    return nearest



