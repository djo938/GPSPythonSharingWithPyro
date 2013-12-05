#http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
#http://blog.perrygeo.net/2007/05/27/python-gpsd-bindings/

from pydaemon import Daemon          #github/djo938
import datetime, os, Pyro4, logging
from gps import *                    #package comes from gpsd
from gps.misc import *               #package comes from gpsd
from utils import getDistance
from simplekml import Kml            #https://pypi.python.org/pypi/simplekml
from data import line_list, point_list

### global vars ###
MAX_SYSTIME_SECONDS_BEFORE_CHANGE = 4
MAX_DELAY_BEFORE_REFRESH          = 5
MAX_DISTANCE_TO_REFRESH           = 2
KML_LINE_POINT_LIMIT              = 200
DISTANCE_LIMIT_TO_BE_NEAR         = 25
KML_LINE_POINT_LIMIT              = 200
MIDDAY                            = (12,30,)
DATA_DIRECTORY                    = "/root/data/kml/"

### google maps icons ###
#http://mabp.kiev.ua/2010/01/12/google-map-markers/
GMAPS_MARKER_POINT = ["http://maps.gstatic.com/mapfiles/ms2/micons/red-dot.png", 
                      "http://maps.gstatic.com/mapfiles/ms2/micons/blue-dot.png", 
                      "http://maps.gstatic.com/mapfiles/ms2/micons/yellow-dot.png", 
                      "http://maps.gstatic.com/mapfiles/ms2/micons/green-dot.png", 
                      "http://maps.gstatic.com/mapfiles/ms2/micons/pink-dot.png", 
                      "http://maps.gstatic.com/mapfiles/ms2/micons/ltblue-dot.png", 
                      "http://maps.gstatic.com/mapfiles/ms2/micons/orange-dot.png", 
                      "http://maps.gstatic.com/mapfiles/ms2/micons/purple-dot.png"]

GMAPS_MARKER_URL    = "http://maps.google.com/mapfiles/marker"
GMAPS_MARKER_COLOUR = ["", "_black", "_brown", "_green", "purple", "yellow", "_grey", "_orange", "_white"] #empty one means red
GMAPS_MARKER_LETTER = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W"]

### function ###
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
                
                #kml vars
                kml_list                = []
                kml_interest_line_list  = []
                kml_interest_point_list = []
                kml                     = None
                
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
                            
                            #find the nearest place (line or point)
                            nearest_line  = findThenearestLine(gpsd.fix.latitude, gpsd.fix.longitud,line_list)
                            nearest_point = findTheNearestPoint(gpsd.fix.latitude, gpsd.fix.longitud,point_list)
                            
                            if nearest_line[0] < nearest_point[0]:
                                nearest = nearest_line
                            else:
                                nearest = nearest_point
                            
                            #share
                            if DISTANCE_LIMIT_TO_BE_NEAR > nearest[0]:
                                proxy.setPlace(nearest[2], nearest[0], nearest[1], utcdatetime)
                                
                                if len(nearest) == 5: #point
                                    pass
                                else:                 #line
                                    pass
                                    #TODO print start, stop or the line, not the three
                                
                                #TODO add in kml interest list
                                    #difference between lines and point
                                    #don't write twice the same interest object on the kml
                                        #keep a dico of already writed object
                                
                            else:
                                proxy.setPlace("", sys.maxint, "", None)
                            
                            ## KML ##
                            kml_list.append( (gpsd.fix.latitude, gpsd.fix.longitude,) )
                            if len(kml_list) > KML_LINE_POINT_LIMIT:
                                if kml == None:
                                    kml = Kml()
                                
                                line = kml.newlinestring(name="", description="", coords=kml_list) #TODO name + descr
                                
                                #if past midday, colour the line in red
                                if utcdatetime == None or utcdatetime.hour < MIDDAY[0] or (utcdatetime.hour == MIDDAY[0] and utcdatetime.minute < MIDDAY[1]):
                                    line.style.linestyle.color = 'afff0000'#morning, blue line
                                else:
                                    line.style.linestyle.color = 'af0000ff'#afternoon, red line
                                
                                #write the meeted line of interest
                                for line in kml_interest_line_list:
                                    line = kml.newlinestring(name="", description="", coords=kml_list) #TODO name + descr +coords
                                    line.style.linestyle.color = 'af00ff00' #green
                                    #from line list
                                    #green line
                                    #start point = http://maps.google.com/mapfiles/dd-start.png
                                    #end point = http://maps.google.com/mapfiles/dd-end.png
                                    
                                #write the meeted point of interest
                                for point in kml_interest_point_list:
                                    point = kml.newpoint(name="dump_"+str(dumpFile.UID)+"_"+dumpTime, description="",coords=[(dumpFile.longitude,dumpFile.latitude)]) #TODO name, description, coords
                                    point.style.iconstyle.icon.href = UIDtoColor[dumpFile.UID] #TODO
                                    #from point list
                                    #from dump done
                                    
                                
                                #save the file (for every line written, overwrite the file)
                                date = datetime.datetime.now
                                kml.save(DATA_DIRECTORY+"skidump_"+str(date.day)+"_"+str(date.month)+"_"+str(date.year)+".kml")
                                
                                #reset list
                                kml_list                = []
                                kml_interest_line_list  = []
                                kml_interest_point_list = []
                                
                            #TODO sqllite (?)
                                #could be interesting in case of prblm to make some search
                                #not realy prior
                            
                        lastpos = (gpsd.fix.latitude,gpsd.fix.longitude,)
                        
                    ### ALTITUDE
                    if not isnan(gpsd.fix.altitude):
                        logging.info("altitude : "+str(gpsd.fix.altitude))
                        proxy.setAltitude(gpsd.fix.altitude, utcdatetime)
                    
                    
                    ### SYSTEM DATETIME ###
                    #TODO don't set time if ntpd was allowed to fetch it
                        #not prior
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
    
    
    
