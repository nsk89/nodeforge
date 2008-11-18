"""
A template for a plugin that does nothing.
See nodeforge/Plugin.py for what a Plugin object has.
"""

from nodeforge.PluginUtils import *

class Main(Plugin):

    def onLoad(self):
        pass

    def onData(self, txt):
        pass
