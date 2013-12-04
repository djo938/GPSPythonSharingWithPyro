#http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
#http://blog.perrygeo.net/2007/05/27/python-gpsd-bindings/

from pydaemon import Daemon
import datetime, os, Pyro4, logging
from gps import *
from gps.misc import *

class sharedGpsClient(object):
    pass #TODO
        #TODO move the code from dumpd about the data sharing to here
            #abstract the use of pyro4 for dumpd

class gpsSharing(Daemon):
    def run(self):
        while True:
            try:
                gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
                proxy=Pyro4.Proxy("PYRONAME:dump.gpsdata")
                timeSet = False
                lastfix = None
                proxy.setGpsLogId(localid)
                while True:
                    gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
                    
                    #define utc datetime
                    utcdatetime = None
                    if gpsd.utc != None and not isnan(gpsd.utc) and len(gpsd.utc) > 0:
                        utcfloatTime = isotime(gpsd.utc)
                        utcdatetime = datetime.datetime.fromtimestamp(int(utcfloatTime))
                    else:
                        pass #TODO
                            #if timeSet == True, use the local time 
                    
                    if not isnan(gpsd.fix.latitude) and not isnan(gpsd.fix.longitude):
                        #TODO if previous fix is bigger than 10 seconds (?) and distant of 2 meters (?)
                            #otherwise, don't compute
                            #if time == None, compute
                    
                        pass #TODO
                        #TODO logging.info("position : "+position)
                        
                        #TODO share
                        
                        #TODO find the nearest place (line or point)
                            
                            #TODO share
                        
                        #TODO kml
                        
                    if not isnan(gpsd.fix.altitude):
                        pass #TODO
                        #TODO logging.info("altitude : "+altitude)
                    
                        #TODO share
                    
                    #set time
                        #TODO only one time ?
                            #or if the difference is 5 seconds ? (for example)
                    if not timeSet and utcdatetime != None: 
                        #TODO
                            #build this line only with utcdatetime
                        newDate = "date -s \""+str(utcdatetime.day)+" "+utcdatetime.strftime("%b")+" "+str(utcdatetime.year)+" "+fixtime[0:2]+":"+fixtime[2:4]+":"+fixtime[4:6]+"\""
                        logging.info(newDate)
                        if os.system(newDate) != 0:
                            logging.warning("failed to set date : "+newDate)
                        else:
                            timeSet = True
                    logging.info("datetime : "+str(utcdatetime))
                    
            except Exception as ex:
                logging.exception("manage data Exception : "+str(ex))
                time.sleep(2)
                continue

if __name__ == "__main__":
    gpsclid = gpsSharing("gpscli")
    gpsclid.main()
    
    
    
