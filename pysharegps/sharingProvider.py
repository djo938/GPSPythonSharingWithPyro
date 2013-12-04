import logging, os, time, sys, Pyro4
from pydaemon import Daemon
from gpsSharedData import sharedGpsData

class dataSharing(Daemon):
    def run(self):
        while True:
            try:
                #create the shared object
                gpsdata=sharedGpsData()

                #init the sharing
                daemon=Pyro4.Daemon() # make a Pyro daemon
                ns=Pyro4.locateNS() # find the name server
                uri=daemon.register(gpsdata) # register the greeting object as a Pyro object
                ns.register("dump.gpsdata", uri) # register the object with a name in the name server

                #start the event loop
                logging.info("Ready. start event loop")
                daemon.requestLoop() # start the event loop of the server to wait for calls
            except Exception as ex:
                logging.exception("sharing provider exception : "+str(ex))
                time.sleep(2)

if __name__ == "__main__":
    dsharing = dataSharing("gpsdatasharing")
    dsharing.main()
