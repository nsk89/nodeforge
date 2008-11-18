"""
An example database plugin.
You can use whatever database you like
or even store pickled python objects.

Do not forget about connection timeouts when connecting
to external databases.
"""

from nodeforge.PluginUtils import *
import sqlite3

class Main(Plugin):

    def onLoad(self):
        """
        Load the sql file.
        """
        
        def newconnection():
            connection = sqlite3.connect('db.sql', isolation_level = None)
            connection.text_factory = str
            return connection
        
        # use these in the main thread
        self.connection = newconnection()
        self.cursor     = self.connection.cursor()
        
        # call this to get a new cursor for a different thread to use
        self.newcursor = lambda: newconnection().cursor()
        
        
        self.cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (op NUMERIC, name  PRIMARY KEY, quit REAL,\
        lastchat TEXT, lastchattime REAL, email NONE, banned NUMERIC)")