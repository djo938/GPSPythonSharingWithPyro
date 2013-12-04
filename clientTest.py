#!/usr/bin/python

from pysharegps import sharedGpsClient
import logging

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)
    client = sharedGpsClient()
    
    if client.isInit():
        position = client.getSharedObject().getPosition()
        print "latitude: "+str(position[0])+", "+str(position[1])+" ("+str(position[2])+")"
        
        altitude = client.getSharedObject().getAltitude()
        print "altitude: "+str(altitude[0])+str(altitude[1])+" ("+str(position[2])+")"
        
        place = client.getSharedObject().getPlace()
        print "nearest place: "+place[0]+" at "+str(place[1])+str(place[2])+" ("+str(position[3])+")"
    else:
        print "fail to init shared object"