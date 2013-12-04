import logging, os, time, sys, Pyro4
from pydaemon import Daemon
from gpsSharedData import sharedGpsData

class dataSharing(Daemon):
    def run(self):
        while True:
            try:
                gpsdata=sharedGpsData()

                daemon=Pyro4.Daemon() # make a Pyro daemon
                ns=Pyro4.locateNS() # find the name server
                uri=daemon.register(gpsdata) # register the greeting object as a Pyro object
                ns.register("dump.gpsdata", uri) # register the object with a name in the name server

                logging.info("Ready.")
                daemon.requestLoop() # start the event loop of the server to wait for calls
            except Exception as ex:
                logging.exception("dump exception : "+str(ex))
                time.sleep(2)

if __name__ == "__main__":
    dsharing = dataSharing("gpsdatasharing")
    dsharing.main()
