from nodeforge.PluginUtils import *

class Main(Plugin):
    def onData(self, raw):
        p = self.parse.context
    
        if p[1] == '001':
            self.parse.join("#nodeforge")
        
    def onLoad(self):
        self.parse = self.core.findPlugin('IRC Parser')