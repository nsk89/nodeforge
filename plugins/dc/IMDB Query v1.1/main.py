from nodeforge.PluginUtils import *
from threading import Thread

dimport('imdblib')

class Main(Plugin):
    def onData(self, raw):
        context = self.parse.context
        
        if context.cmd == '/tv':
            Thread(target=self.getEpisode, args=(self.parse.context,)).start()
    
    def onLoad(self):
        """
        Load the parser.
        """
        self.parse = self.core.findPlugin('NMDC Parser')
        
    def getEpisode(self, context):
        """
        This is the command to get the TV listings.
        It could take a while so it must run on another thread.
        """
        msg = context.sender+': '+imdblib.getEps(context.args)
        context.tell(msg)