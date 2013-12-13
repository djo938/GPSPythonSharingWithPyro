#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser, datetime

### google maps icons ###
#http://mabp.kiev.ua/2010/01/12/google-map-markers/
#GMAPS_MARKER_POINT = ["http://maps.gstatic.com/mapfiles/ms2/micons/red-dot.png", 
#                      "http://maps.gstatic.com/mapfiles/ms2/micons/blue-dot.png", 
#                      "http://maps.gstatic.com/mapfiles/ms2/micons/yellow-dot.png", 
#                      "http://maps.gstatic.com/mapfiles/ms2/micons/green-dot.png", 
#                      "http://maps.gstatic.com/mapfiles/ms2/micons/pink-dot.png", 
#                      "http://maps.gstatic.com/mapfiles/ms2/micons/ltblue-dot.png", 
#                      "http://maps.gstatic.com/mapfiles/ms2/micons/orange-dot.png", 
#                      "http://maps.gstatic.com/mapfiles/ms2/micons/purple-dot.png"]

from simplekml import Kml            #https://pypi.python.org/pypi/simplekml

GMAPS_MARKER_URL    = "http://maps.google.com/mapfiles/marker"
GMAPS_MARKER_COLOUR = ["", "_black", "_brown", "_green", "purple", "yellow", "_grey", "_orange", "_white"]
GMAPS_MARKER_LETTER = ["","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W"]
DEFAULT_COLOR = ""
DEFAULT_LETTER = ""

class kmlManager(object):
    def init(self):
        self.kml_list_start_time               = None
        self.kml_list                          = []
        self.kml_interest_line_list            = []
        self.kml_interest_point_list           = []
        
    def __init__(self, line_limit_point, pathDirectory):
        self.kml = Kml()
        self.init()
        self.kml_interest_line_already_meeted  = {}
        self.kml_interest_point_already_meeted = {}
        self.line_limit_point                  = line_limit_point
        self.pathDirectory = pathDirectory
        self.midday = (12,0,)
    
    def addPointOfInterest(self,point):
        if point.descr not in self.kml_interest_point_already_meeted: #not yet printed ?
            self.kml_interest_point_already_meeted[point.descr] = True
            self.kml_interest_point_list.append(point)

    def addLineOfInterest(self, line):
        if line.descr not in self.kml_interest_line_already_meeted: #not yet printed ?
            self.kml_interest_line_already_meeted[line.descr] = True
            self.kml_interest_line_list.append(line)
            
    def addLinePoint(self,gpoint, utcdatetime, colorMarker):
        if self.line_limit_point > 0:#don't want to write the line of the road ?
            if len(self.kml_list) == 0: #set start time
                self.kml_list_start_time = utcdatetime
                
            self.kml_list.append( (gpoint.lat, gpoint.lon,) )
        
        if len(self.kml_list) >= self.line_limit_point:
            #kml process
            if len(self.kml_list) > 0:
                line = self.kml.newlinestring(name="From "+self.kml_list_start_time.isoformat()+" to "+utcdatetime.isoformat(), description="", coords=self.kml_list)
            
                #if past midday, colour the line in red
                if utcdatetime.hour < self.midday[0] or (utcdatetime.hour == self.midday[0] and utcdatetime.minute < self.midday[1]):
                    line.style.linestyle.color = 'afff0000'#morning, blue line
                else:
                    line.style.linestyle.color = 'af0000ff'#afternoon, red line
            
            #write the meeted line of interest
            for interest_line in self.kml_interest_line_list:
                #line
                line = self.kml.newlinestring(name=interest_line.descr, description="", coords=((interest_line.start.lat,interest_line.start.lon,), (interest_line.end.lat,interest_line.end.lon,),))
                line.style.linestyle.color = 'af00ff00' #green
                
                #start point
                point = self.kml.newpoint(name="Start point of "+interest_line[2], description="",coords=(interest_line.start.lat,interest_line.start.lon,))
                point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/dd-start.png"
                
                #end point
                point = self.kml.newpoint(name="End point of "+interest_line[2], description="",coords=(interest_line.end.lat,interest_line.end.lon,))
                point.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/dd-end.png"
                
            #write the meeted point of interest
            for interest_point in self.kml_interest_point_list:
                point = self.kml.newpoint(name=interest_point.name, description=interest_point.descr,coords=( (interest_point.lat, interest_point.lon,), ))
                point.style.iconstyle.icon.href = colorMarker.getColorPath(interest_point.name)
           
            #save the file (for every line written, overwrite the file)
            date = datetime.datetime.now()
            self.kml.save(self.pathDirectory+"skidump_"+str(date.day)+"_"+str(date.month)+"_"+str(date.year)+".kml")
            
            #reset list
            self.init()

    def addEventPointList(self,l):
        #get point of interest from proxy
        self.kml_interest_point_list.extend(l)

class ColorMarkerConfigManager(object):
    def __init__(self, path = None):
        self.marker = {}
        self.usedCouple = {}
        self.path = path
        
    def loadConfig(self):
        #reset marker
        self.marker = {}
        self.usedCouple = {}
    
        if self.path == None:
            return
    
        #file exist ?
        if not os.path.exists(self.path):
            return
    
        #load config
        config = ConfigParser.RawConfigParser()
        config.read(self.path)
        
        waiting_list = {}
        waiting = False
        
        for s in config.sections():
            waiting = False
        
            #COLOR MANAGEMENT
            if config.has_option(s,"color"):
                color = config.get(s, "color").lower()
            else:
                color = DEFAULT_COLOR
                
            if color == "red":
                color = ""
            
            indexc = 0
            try:
                if len(color) == 0:
                    indexc = GMAPS_MARKER_COLOUR.index(color)
                else:
                    indexc = GMAPS_MARKER_COLOUR.index("_"+color)
            except ValueError:
                waiting = True
            
            #LETTER MANAGEMENT
            if config.has_option(s,"letter"):
                letter = config.get(s, "letter").lower()
            else:
                letter = DEFAULT_LETTER
            
            letter = letter.upper()
            indexl = 0
            try:
                indexl = GMAPS_MARKER_LETTER.index(letter)
            except ValueError:
                print "plop ", letter
                waiting = True
    
            if waiting:
                waiting_list[s] = (indexc, indexl)
            else:
                self.marker[s] = (indexc, indexl)
                self.usedCouple[(indexc, indexl)] = True
                
        if len(waiting_list) > 0:
            for k,v in waiting_list.iteritems():
                c,l = self._getNextAvailableColor(v[0],v[1])
                
                self.marker[k] = (c, l)
                self.usedCouple[(c, l)] = True
            self.saveConfig()
    
        #http://docs.python.org/2/library/configparser.html
        #set dico(name:color) in global
        #must be load at the running time
            #the conf file must be updated every time the service restart.
        #put the call of this function somewhere
    
    def _getNextAvailableColor(self, indexc = 0, indexl = 1):
        for i in range(indexc, len(GMAPS_MARKER_COLOUR)):
            for j in range(indexl, len(GMAPS_MARKER_LETTER)):
                if (i,j,) in self.usedCouple:
                    continue
                else:
                    return i,j
        
        return 0,0 #default if no more combination available
    
    def getColorPath(self, name):
        #the name is in the dico ? return its color
        if name in self.marker:
            return GMAPS_MARKER_URL+GMAPS_MARKER_COLOUR[self.marker[name][0]]+GMAPS_MARKER_LETTER[self.marker[name][1]]+".png"
    
        #we've got a new name 
        c,l = self._getNextAvailableColor()
        self.marker[name] = (c, l)
        self.usedCouple[(c, l)] = True
    
        self.saveConfig()
        
        return GMAPS_MARKER_URL+GMAPS_MARKER_COLOUR[c]+GMAPS_MARKER_LETTER[l]+".png"
        
    def saveConfig(self):
        if self.path == None:
            return
    
        config = ConfigParser.RawConfigParser()
        for section in self.marker.keys():
            #print "save", section, GMAPS_MARKER_COLOUR[self.marker[section][0]], GMAPS_MARKER_LETTER[self.marker[section][1]]
            config.add_section(section)
            color = GMAPS_MARKER_COLOUR[self.marker[section][0]]
            
            if color.startswith("_"):
                color = color[1:]
            
            config.set(section, 'color', color)
            config.set(section, 'letter', GMAPS_MARKER_LETTER[self.marker[section][1]])

        with open(self.path, 'wb') as configfile:
            config.write(configfile)

