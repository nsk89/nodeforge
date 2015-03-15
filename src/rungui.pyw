#!/usr/bin/env python
"""
The file for running the GUI
"""

import sys, os, code
from threading import Thread

from nodeforge.gui.application import Application
 
app = Application()
Thread(target=app.mainloop).start()

# point the stds to the gui
sys.stdout = app.stdout
sys.stderr = app.stderr

# Echo the inputs
def inputecho(data):
    app.stdout.write("> "+data+"\n")
app.input.callOnInput(inputecho)

# insert framework configuration here.
from configure import *

code.interact(readfunc=app.input.raw_input(), local=locals())
