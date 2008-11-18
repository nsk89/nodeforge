"""
A generic reconnector plugin.
"""

from nodeforge.PluginUtils import *
from twisted.internet import reactor
from twisted.internet.error import ConnectionDone

class Main(Plugin):
    
    reconnect_event = None
    try_reconnect = True
    
    def onConnectFailed(self, reason):
        if self.reconnect_event == None:
            self.reconnect()
    
    def onDisconnect(self, reason):
        if self.reconnect_event == None:
            self.reconnect()
            
    def onConnect(self):
        if self.reconnect_event != None:
            self.reconnect_event = None
        
    def reconnect(self):
        self.reconnect_event = reactor.callLater(60, self.core.connect)