#http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
#http://blog.perrygeo.net/2007/05/27/python-gpsd-bindings/

from pydaemon import Daemon          #github/djo938
import datetime, os, Pyro4, logging
from gps import *                    #package comes from gpsd
from gps.misc import *               #package comes from gpsd
from utils import *
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
CONF_DIRECTORY                    = "/root/conf/gpscli/"
PYRO_NAMING                       = "PYRONAME:dump.gpsdata2"

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

def manageFixTime(gpsd, timeSet)
    utcdatetime = None
    
    #try to get the time of the fix
    if gpsd.utc != None and not isnan(gpsd.utc) and len(gpsd.utc) > 0:
        utcfloatTime = isotime(gpsd.utc)
        utcdatetime = datetime.datetime.fromtimestamp(int(utcfloatTime))
    
        #set system time
        #TODO don't set system time if ntpd fetch it
            #not prior
        if not timeSet:
            timeSet = setSystemTime(utcdatetime)
        else:
            currentSystemTime = datetime.datetime.now()
            if (currentSystemTime - utcdatetime).total_seconds() > MAX_SYSTIME_SECONDS_BEFORE_CHANGE:
                setSystemTime(utcdatetime)
    else:
        #if gps fix does not have datetime, use the system time
        logging.warning("no time set in the gps fix, use the local time")
        utcdatetime = datetime.datetime.now() #if timeSet == False, the current time could be hazardous
    
    logging.info("datetime : "+str(utcdatetime))
    logging.info("timeSet : "+str(timeSet))
    
    return timeSet, utcdatetime

def manage_kml(utcdatetime, kml, kml_list, kml_interest_line_list, kml_interest_point_list):
    if len(kml_list) > 0:
        line = kml.newlinestring(name="From "+kml_list_start_time.isofromat()+" to "+utcdatetime.isoformat, description="", coords=kml_list)
    
        #if past midday, colour the line in red
        if utcdatetime.hour < MIDDAY[0] or (utcdatetime.hour == MIDDAY[0] and utcdatetime.minute < MIDDAY[1]):
            line.style.linestyle.color = 'afff0000'#morning, blue line
        else:
            line.style.linestyle.color = 'af0000ff'#afternoon, red line
    
    #write the meeted line of interest
    for interest_line in kml_interest_line_list:
        #line
        line = kml.newlinestring(name=interest_line.descr, description="", coords=((interest_line.start.lat,interest_line.start.lon,), (interest_line.end.lat,interest_line.end.lon,),))
        line.style.linestyle.color = 'af00ff00' #green
        
        #start point
        point = kml.newpoint(name="Start point of "+interest_line[2], description="",coords=(interest_line.start.lat,interest_line.start.lon,))
        point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/dd-start.png"
        
        #end point
        point = kml.newpoint(name="End point of "+interest_line[2], description="",coords=(interest_line.end.lat,interest_line.end.lon,))
        point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/dd-end.png"
        
    #write the meeted point of interest
    for interest_point in kml_interest_point_list:
        point = kml.newpoint(name=interest_point.name, description=interest_point.descr,coords=( (interest_point.lat, interest_point.lon,), ))
        point.style.iconstyle.icon.href = getColorPath(interest_point.name)
   
    #save the file (for every line written, overwrite the file)
    date = datetime.datetime.now
    kml.save(DATA_DIRECTORY+"skidump_"+str(date.day)+"_"+str(date.month)+"_"+str(date.year)+".kml")

def loadColorConf():
    #http://docs.python.org/2/library/configparser.html
    #set dico(name:color) in global
    #must be load at the running time
        #the conf file must be updated every time the service restart.
    #put the call of this function somewhere
    
    pass #TODO

def getColorPath(name):
    #TODO the name is in the dico ? return its color
    
    #TODO if the name is not in the dico, compute the next available color
    
    #TODO save the conf file CONF_DIRECTORY+"marker.conf"
    
    return GMAPS_MARKER_POINT[0]

def manageSqlLite(utcdatetime, gpoint):
    #TODO sqllite (?)
    #could be interesting in case of prblm to make some search
    #not realy prior
    
    pass #TODO

class gpsSharing(Daemon):
    def run(self):
        while True:
            try:
                gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
                proxy=Pyro4.Proxy(PYRO_NAMING)
                timeSet = False
                lastfix = None
                lastpos = (0.0, 0.0, )
                proxy.setGpsLogId(localid)
                
                #kml vars
                kml_list_start_time               = None
                kml_list                          = []
                kml_interest_line_list            = []
                kml_interest_line_already_meeted  = {}
                kml_interest_point_list           = []
                kml_interest_point_already_meeted = {}
                kml                               = Kml()
                
                while True:
                    gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
                    
                    ### DATETIME ###
                    timeSet, utcdatetime = manageFixTime(timeSet, gpsd)
                    
                    ### ALTITUDE
                    if not isnan(gpsd.fix.altitude):
                        logging.info("altitude : "+str(gpsd.fix.altitude))
                        proxy.setAltitude(gpsd.fix.altitude, utcdatetime)
                    
                    ### POSITION ###
                    
                    #if position is not set, nothing to do
                    if isnan(gpsd.fix.latitude) or isnan(gpsd.fix.longitude):
                        continue
                    
                    #if no fix time OR previous fix is bigger than 10 seconds (?) OR distant of 2 meters (?)
                        #otherwise, don't compute
                        #if time == None, compute
                    gpoint = gpsPoint(gpsd.fix.latitude, gpsd.fix.longitude)
                    logging.info("position : "+str(gpsd.fix.latitude)+","+str(gpsd.fix.longitude))
                    
                    #if no need to refresh position
                    if lastfix != None and (utcdatetime - lastfix).total_seconds() <= MAX_DELAY_BEFORE_REFRESH and getDistance(gpoint, lastpos) <= MAX_DISTANCE_TO_REFRESH:
                        continue

                    #share the position
                    proxy.setPosition(gpsd.fix.latitude, gpsd.fix.longitude, utcdatetime)
                    
                    ### PLACE ###
                    
                    #find the nearest place (line or point)
                    #TODO possible to hide the 7 lines of code in the utils part
                        #create a special gpsObject, a list of point that make a line
                            #this object can have 1, 2 or many point
                        #generic method to compute distance
                            #from each line between two consecutive point
                            #from each point 
                    nearest_line  = findThenearestLine(gpoint)
                    nearest_point = findTheNearestPoint(gpoint)
                    
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

                        #add in kml ?
                        if nearest_point.descr not in kml_interest_point_already_meeted: #not yet printed ?
                            kml_interest_point_already_meeted[nearest_point.descr] = True
                            kml_interest_point_list.append(nearest_point)
                        
                    elif nearest_line != None and nearest_line.distance < DISTANCE_LIMIT_TO_BE_NEAR:
                        #share
                        proxy.setPlace(nearest_line.descr, nearest_line.distance, nearest_line.distFrom, utcdatetime)
                        
                        #add in kml ?
                        if nearest_line.descr not in kml_interest_line_already_meeted: #not yet printed ?
                            kml_interest_line_already_meeted[nearest_line.descr] = True
                            kml_interest_line_list.append(nearest_line)
                    else:
                        proxy.setPlace("", sys.maxint, "", None)
                        
                    ### KML ###
                    if KML_LINE_POINT_LIMIT > 0:#don't want to write the line of the road ?
                        if len(kml_list) == 0: #set start time
                            kml_list_start_time = utcdatetime
                            
                        kml_list.append( (gpoint.lat, gpoint.lon,) )
                    
                    if len(kml_list) > KML_LINE_POINT_LIMIT:
                        #get point of interest from proxy
                        kml_interest_point_list.append(proxy.getAndResetPointOfInterest())
                        
                        #kml process
                        manage_kml(utcdatetime, kml, kml_list, kml_interest_line_list, kml_interest_point_list)
                        
                        #reset list
                        kml_list                = []
                        kml_interest_line_list  = []
                        kml_interest_point_list = []
                    
                    ### SQL LITE ###
                    manageSqlLite(utcdatetime, gpoint)
                    
                    #set next iteration variable
                    lastpos = gpoint
                    lastfix = utcdatetime
            except Exception as ex:
                logging.exception("manage data Exception : "+str(ex))
                time.sleep(2)
                continue

class sharedGpsClient(object):
    def __init__(self):
        self.reInit()
    
    def isInit(self):
        return self.shared == None
        
    def reInit(self):
        try:
            self.shared = Pyro4.Proxy(PYRO_NAMING)
        except Exception as ex:
            self.shared = None
            logging.exception("Pyro4 Exception (getPosition) : "+str(ex))
    
    def getSharedObject(self):
        return self.shared

if __name__ == "__main__":
    gpsclid = gpsSharing("gpscli")
    gpsclid.main()
    
    
    
