"""
This file should be imported at the bottom of configure.py

TODO:
All of this may be moved into a single function in the future
so people can choose a reactor in configure.py
"""

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from threading import currentThread, Thread

# Check to see if main thread is alive
mainthread = currentThread()
def checkExit():
    if not mainthread.isAlive():
        reactor.stop()

# Every second, make sure that the interface thread is alive.
LoopingCall(checkExit).start(1)

# start the network loop in a new thread
Thread(target=lambda : reactor.run(installSignalHandlers=0)).start()