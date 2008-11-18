"""
Configuration file.
Edit the clients and servers you need here.
"""

from nodeforge.cores.client import Client

#dcbot = Client(address='someaddress.com', port=12345, folder='plugins/dc', nick='nodeforge')
ircbot = Client(address='irc.freenode.net', port=6667, folder='plugins/irc', nick='nodeforge')

# Do not edit below
import nodeforge.StartEngine