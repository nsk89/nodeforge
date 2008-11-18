#!/usr/bin/env python
"""
The GUI object
"""
from Tkinter import *

from nodeforge.gui.TextBox import TextBox
from nodeforge.gui.SmartInput import SmartInput

class Application(Tk):
    def __init__(self, **kw):
        Tk.__init__(self, **kw)
        
        self.title('GUI')
        self.resizable(True,True)
        
        self.grid_columnconfigure(0,weight=1)
        
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=3)
        
        
        self.status = Label(self, text='Status', relief=SUNKEN, bd=1)
        self.input = SmartInput(self, font=("Courier",10))
        
        
        self.stderr = TextBox(self, height=10, font=("Courier", 9), state=DISABLED)
        self.stdout = TextBox(self, height=15, font=("Courier", 9), state=DISABLED)
        
        
        self.stderr.grid(row=0, column=0, sticky='NWES')
        self.stdout.grid(row=1, column=0, sticky='NWES')
        self.input.grid(row=2, column=0, columnspan=2, sticky='EW')
        self.status.grid(row=3, column=0, columnspan=2, sticky='EW')
        
        self.stderr.write('>> Error Logging\n')
        self.stdout.write('>> Welcome\n')
        
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        
    def onClose(self):
        """
        Close the interpreter thread if the gui is closed.
        TODO: close the communications thread.
        """
        self.input.announceInput('exit()')
        
        self.destroy()
        os._exit(0)