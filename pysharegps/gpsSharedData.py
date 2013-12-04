

class sharedGpsData(object):
    def __init__(self):
        self.pos   = (0.0,0.0,None,)   # float latitude(from equateur),float longitude(from greenwitch),datetime (Universal Time Coordinated)
        self.alt   = (0.0, "M", None,) # float altitude, string scale unit, datetime (Universal Time Coordinated)
        self.place = ("",0, None, )       # string place name, distance from this point, datetime (Universal Time Coordinated)
    
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
    def setPlace(self, placename, distance, dtime):
        self.place = (placename, distance, dtime,)
        
    def getPlace(self):
        return self.place
