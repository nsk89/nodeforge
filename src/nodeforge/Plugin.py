class Plugin(object):
    """
    All plugin files ( __init__.py files ) should have a class called "Main" which 
    inherits and extends this class.
    """
    # warning, changing priority does nothing until you update the order in the core.
    priority = 0
    name     = 'Untitled Plugin'
    
    def onData(self, context): pass
    def onConnect(self): pass
    def onConnectFailed(self, reason): pass
    def onDisconnect(self, reason): pass
    def onLoad(self): pass
        
    def onUnload(self):
        del self
        
        
class Priority(object):
    """
    An enum to use for plugin priority levels.
    """
    
    parser = -10000
    
    high   = -5000
    normal = 0
    low    = 5000