from nodeforge.PluginUtils import *

import urllib2, copy
from BeautifulSoup import BeautifulSoup
from threading import Thread

class Main(Plugin):

    def onLoad(self):
        """
        Load the parser.
        """
        self.parse = self.core.findPlugin('NMDC Parser')


    def onData(self, txt):
        context = self.parse.context
        
        if context.cmd == '/temp' or context.cmd == '/weather':
            Thread(target=lambda:self.getWeather(copy.copy(context))).start()
    
    def getWeather(self, context):
        context.reply(self.weatherTxt())
        
    def weatherTxt(self):
        req = urllib2.Request("http://www.cornell.edu/about/status/weather.cfm")
        
        try:
            response = urllib2.urlopen(req).read()
        except:
            return "Connection error, please try again."
        
        soup = BeautifulSoup(response)
        
        try:
            tempF = soup.find(id="currenttemperatureF").string.strip().replace("&deg;","")
            tempC = soup.find(id="currenttemperatureC").string.strip().replace("&deg;","")
            
            description = soup.find(id="currentweather").findAll("li")
            updated = soup.find(attrs={"class":"lastupdated"}).string.strip()
            
            newdesc = ""
            
            for line in description:
                newdesc += " - "+line.string.strip()
                
            newdesc += " - "+updated
            newdesc = ("%s/%s " % (tempF,tempC)) + newdesc
            
            return newdesc 
        except:
            return "Error parsing the website."