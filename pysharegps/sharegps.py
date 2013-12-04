#http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
#http://blog.perrygeo.net/2007/05/27/python-gpsd-bindings/

from pydaemon import Daemon          #github/djo938
import datetime, os, Pyro4, logging
from gps import *                    #package comes from gpsd
from gps.misc import *               #package comes from gpsd
from utils import getDistance

MAX_SYSTIME_SECONDS_BEFORE_CHANGE = 10
MAX_DELAY_BEFORE_REFRESH = 10
MAX_DISTANCE_TO_REFRESH = 2

def setSystemTime(dtime):
    newDate = "date -s \""+dtime.strftime("%d %b %Y %H:%M:%S")+"\""
    logging.info(newDate)
    if os.system(newDate) != 0:
        logging.warning("failed to set date : "+newDate)
        return False
    return True

class sharedGpsClient(object):
    def __init__(self):
        self.reInit()
    
    def isInit(self):
        return self.shared == None
        
    def reInit(self):
        try:
            self.shared = Pyro4.Proxy("PYRONAME:dump.gpsdata")
        except Exception as ex:
            self.shared = None
            logging.exception("Pyro4 Exception (getPosition) : "+str(ex))
    
    def getSharedObject(self):
        return self.shared


class gpsSharing(Daemon):
    def run(self):
        while True:
            try:
                gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
                proxy=Pyro4.Proxy("PYRONAME:dump.gpsdata")
                timeSet = False
                lastfix = None
                lastpos = (0.0, 0.0, )
                proxy.setGpsLogId(localid)
                while True:
                    gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
                    currentSystemTime = datetime.datetime.now() #get the current system timec 
                    
                    ### FIX TIME ###
                    #define utc datetime
                    utcdatetime = None
                    
                    #try to get the time of the fix
                    if gpsd.utc != None and not isnan(gpsd.utc) and len(gpsd.utc) > 0:
                        utcfloatTime = isotime(gpsd.utc)
                        utcdatetime = datetime.datetime.fromtimestamp(int(utcfloatTime))
                    
                    #time has already be set ? yes, get the current time of the system
                    elif timeSet: 
                        utcdatetime = datetime.datetime.now()
                    
                    lastfix = utcdatetime
                    
                    ### POSITION ###
                    if not isnan(gpsd.fix.latitude) and not isnan(gpsd.fix.longitude):
                        #if no fix time OR previous fix is bigger than 10 seconds (?) OR distant of 2 meters (?)
                            #otherwise, don't compute
                            #if time == None, compute
                        if utcdatetime == None or (lastfix != None and (utcdatetime - lastfix).total_seconds() > MAX_DELAY_BEFORE_REFRESH or getDistance(gpsd.fix.latitude, gpsd.fix.longitude, lastpos[0], lastpos[1]) > MAX_DISTANCE_TO_REFRESH):
                            logging.info("position : "+str(gpsd.fix.latitude)+","+str(gpsd.fix.longitude))
                            
                            #share
                            proxy.setPosition(gpsd.fix.latitude, gpsd.fix.longitude, utcdatetime)
                            
                            #TODO find the nearest place (line or point)
                                #TODO share
                        
                            #TODO kml (from simplekml import Kml)
                                #see file parse.py
                            
                            #TODO sqllite (?)
                                #could be interesting in case of prblm to make some search
                            
                        lastpos = (gpsd.fix.latitude,gpsd.fix.longitude,)
                        
                    ### ALTITUDE
                    if not isnan(gpsd.fix.altitude):
                        logging.info("altitude : "+str(gpsd.fix.altitude))
                        proxy.setAltitude(gpsd.fix.altitude, utcdatetime)
                    
                    
                    ### SYSTEM DATETIME ###
                    #TODO don't set time if ntpd was allowed to fetch it
                    if utcdatetime != None:
                        if not timeSet:
                            timeSet = setSystemTime(utcdatetime)
                        else:
                            currentSystemTime = datetime.datetime.now()
                            if (currentSystemTime - utcdatetime).total_seconds() > MAX_SYSTIME_SECONDS_BEFORE_CHANGE:
                                setSystemTime(utcdatetime)
                        
                    logging.info("datetime : "+str(utcdatetime))
                    
            except Exception as ex:
                logging.exception("manage data Exception : "+str(ex))
                time.sleep(2)
                continue

if __name__ == "__main__":
    gpsclid = gpsSharing("gpscli")
    gpsclid.main()
    
    
    
