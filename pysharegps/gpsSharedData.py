
import sys
from utils import gpsPoint

class sharedGpsData(object):
    def __init__(self):
        self.pos   = (0.0,0.0,None,)   # float latitude(from equateur),float longitude(from greenwitch),datetime (Universal Time Coordinated)
        self.alt   = (0.0, "M", None,) # float altitude, string scale unit, datetime (Universal Time Coordinated)
        self.place = ("",sys.maxint,"M", "", None, )       # string place name, distance from this point, datetime (Universal Time Coordinated)
        self.point_to_print = []
        self.gpsShareDaemonId = -1
    
    ###

    def setGpsLogId(self, process_id):
        self.gpsShareDaemonId = process_id

    def getGpsLogId(self):
        return self.gpsShareDaemonId

    ###
    def setPosition(self, latitude, longitude, dtime):
        self.pos = (latitude, longitude, dtime,)
        
    def getPosition(self):
        return self.pos
    
    ### 
    def setAltitude(self, altitude, dtime, unit = "M"):
        self.alt = (altitude, unit, dtime,)
        
    def getAltitude(self):
        return self.alt
        
    ###
    def setPlace(self, placename, distance, distanceType, dtime, unit = "M"):
        self.place = (placename, distance, unit, distanceType, dtime,)
        
    def getPlace(self):
        return self.place
        
    ###
    def addPointOfInterest(self, lat, lon, key, descr=None):
        self.point_to_print.append(gpsPoint(lat, lon, key, descr))
        
    def getAndResetPointOfInterest(self):
        toRet = self.point_to_print
        self.point_to_print = []
        return toRet
