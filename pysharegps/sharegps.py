#http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
#http://blog.perrygeo.net/2007/05/27/python-gpsd-bindings/

from pydaemon import Daemon          #github/djo938
import datetime, os, Pyro4, logging
from gps import *                    #package comes from gpsd
from gps.misc import *               #package comes from gpsd
from utils import *
from data import line_list, point_list
import dateutil.parser               #https://pypi.python.org/pypi/python-dateutil
from kmlManagement import ColorMarkerConfigManager, kmlManager

### global vars ###
MAX_SYSTIME_SECONDS_BEFORE_CHANGE = 4
MAX_DELAY_BEFORE_REFRESH          = 5
MAX_DISTANCE_TO_REFRESH           = 2
DISTANCE_LIMIT_TO_BE_NEAR         = 25
KML_LINE_POINT_LIMIT              = 10 #200 TODO set to default
MIDDAY                            = (12,30,)
DATA_DIRECTORY                    = "/root/data/kml/"
CONF_DIRECTORY                    = "/root/conf/gpscli/"
PYRO_NAMING                       = "PYRONAME:dump.gpsdata2"

### function ###
def setSystemTime(dtime):
    newDate = "date -s \""+dtime.strftime("%d %b %Y %H:%M:%S")+"\""
    logging.info(newDate)
    if os.system(newDate) != 0:
        logging.warning("failed to set date : "+newDate)
        return False
    return True

def manageFixTime(gpsd, timeSet):
    utcdatetime = None
    
    #try to get the time of the fix
    print gpsd.__class__, type(gpsd),type(gpsd.utc), gpsd.utc
    if gpsd.utc != None and len(str(gpsd.utc)) > 0:# and not isnan(gpsd.utc):
        #utcfloatTime = isotime(gpsd.utc)
        #utcdatetime = datetime.datetime.fromtimestamp(int(utcfloatTime))
        utcdatetime = dateutil.parser.parse(gpsd.utc)
        utcdatetime = utcdatetime.replace(tzinfo=None)
        
        #set system time
        #TODO don't set system time if ntpd fetch it
            #not prior
        if not timeSet:
            timeSet = setSystemTime(utcdatetime)
        else:
            currentSystemTime = datetime.datetime.now()
            #currentSystemTime = currentSystemTime.replace(tzinfo=None)
            if (currentSystemTime - utcdatetime).total_seconds() > MAX_SYSTIME_SECONDS_BEFORE_CHANGE:
                setSystemTime(utcdatetime)
    else:
        #if gps fix does not have datetime, use the system time
            #occur at the bigining
        logging.warning("no time set in the gps fix, use the local time")
        utcdatetime = datetime.datetime.now() #if timeSet == False, the current time could be hazardous
    
    
    logging.info("datetime : "+str(utcdatetime))
    logging.info("timeSet : "+str(timeSet))
    
    return timeSet, utcdatetime

def manageSqlLite(utcdatetime, gpoint):
    #TODO sqllite (?)
    #could be interesting in case of prblm to make some search
    #not realy prior
    
    pass #TODO

class gpsSharing(Daemon):
    def run(self):
        while True:
            try:
                gpsd                              = gps(mode=WATCH_ENABLE) #starting the stream of info
                proxy                             = Pyro4.Proxy(PYRO_NAMING)
                timeSet                           = False
                lastfix                           = None
                lastpos                           = (0.0, 0.0, )
                kmlm                              = kmlManager(KML_LINE_POINT_LIMIT, DATA_DIRECTORY)
                kmlm.midday                       = MIDDAY
                colorMarker                       = ColorMarkerConfigManager(CONF_DIRECTORY+"marker.conf")
                proxy.setGpsLogId(self.localid)

                while True:
                    gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
                    ### DATETIME ###
                    timeSet, utcdatetime = manageFixTime(gpsd, timeSet)
                    
                    ### ALTITUDE
                    if not isnan(gpsd.fix.altitude):
                        logging.info("altitude : "+str(gpsd.fix.altitude))
                        proxy.setAltitude(gpsd.fix.altitude, utcdatetime)
                    
                    ### POSITION ###
                    
                    #if position is not set, nothing to do
                    if isnan(gpsd.fix.latitude) or isnan(gpsd.fix.longitude) or (gpsd.fix.latitude == 0.0 and gpsd.fix.longitude == 0.0):
                        continue
                    
                    #if no fix time OR previous fix is bigger than 10 seconds (?) OR distant of 2 meters (?)
                        #otherwise, don't compute
                        #if time == None, compute
                    gpoint = gpsPoint(gpsd.fix.latitude, gpsd.fix.longitude)
                    logging.info("position : "+str(gpsd.fix.latitude)+","+str(gpsd.fix.longitude))
                    
                    #if no need to refresh position
                    print "<",utcdatetime,"><",lastfix,">"
                    if lastfix != None and (utcdatetime - lastfix).total_seconds() <= MAX_DELAY_BEFORE_REFRESH and getDistance(gpoint, lastpos) <= MAX_DISTANCE_TO_REFRESH:
                        continue

                    #share the position
                    proxy.setPosition(gpsd.fix.latitude, gpsd.fix.longitude, utcdatetime)
                    
                    ### PLACE ###
                    
                    #find the nearest place (line or point)
                    #TODO possible to hide the 7 following lines of code in the utils part
                        #create a special gpsObject, a list of point that make a line
                            #this object can have 1, 2 or many point
                        #generic method to compute distance
                            #from each line between two consecutive point
                            #from each point 
                    nearest_line  = findThenearestLine(gpoint, line_list)
                    nearest_point = findTheNearestPoint(gpoint, point_list)
                    
                    #keep only the best
                    if nearest_line != None and nearest_point != None:
                        if nearest_line.distance < nearest_point.distance:
                            nearest_point = None
                        else:
                            nearest_line = None
                    
                    #share the place
                    if nearest_point != None and nearest_point.distance < DISTANCE_LIMIT_TO_BE_NEAR:
                        #share
                        proxy.setPlace(nearest_point.descr, nearest_point.distance, "from point", utcdatetime)
                        kmlm.addPointOfInterest(nearest_point)
                    elif nearest_line != None and nearest_line.distance < DISTANCE_LIMIT_TO_BE_NEAR:
                        #share
                        proxy.setPlace(nearest_line.descr, nearest_line.distance, nearest_line.distFrom, utcdatetime)
                        kmlm.addLineOfInterest(nearest_line)
                    else:
                        #no defined place
                        proxy.setPlace("", sys.maxint, "", None)
                        
                    ### KML ###
                    ipoint = proxy.getAndResetPointOfInterest()
                    for lat, lon, key, descr in ipoint:
                        kmlm.addEventPointList(gpoint(lat, lon, key, descr))
                    
                    kmlm.addLinePoint(gpoint,utcdatetime, colorMarker)
                    
                    ### SQL LITE ###
                    manageSqlLite(utcdatetime, gpoint)
                    
                    #set next iteration variable
                    lastpos = gpoint
                    lastfix = utcdatetime
            except Exception as ex:
                logging.exception("manage data Exception : "+str(ex))
                if self.debug:
                    exit()
                time.sleep(2)
                continue

class sharedGpsClient(object):
    def __init__(self):
        self.reInit()
    
    def isInit(self):
        return self.shared != None
        
    def reInit(self):
        try:
            self.shared = Pyro4.Proxy(PYRO_NAMING)
        except Exception as ex:
            self.shared = None
            logging.exception("Pyro4 Exception (init shared client) : "+str(ex))
    
    def getSharedObject(self):
        return self.shared

if __name__ == "__main__":
    gpsclid = gpsSharing("gpscli")
    gpsclid.main()
    
    
    
