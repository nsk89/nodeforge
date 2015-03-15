"""
Smart Input Box

A heavily featured entry widget for processing user input.

It sends multilined text with a linefeed appended to the end.
Input is received by a blocking function created by raw_input()
Additional features include selection of the entire block when focused on.
The box is also selected when the user presses enter for easy deletion if needed.

Select all and tabbing is implemented.

TODO:
UP/DOWN history box
Crtl+backspace deletion
Autocomplete
"""

from Tkinter import *
from Queue import Queue


class SmartInput(Entry, object):
    
    historySize = 20
    historyIndex = 0
    
    def __init__(self, master=None, cnf={}, **kw):
        Entry.__init__(self, master, cnf, takefocus=False, **kw)
        
        self.alert      = []
        self.alertFuncs = []
        
        self.history    = []
                
        self.bind('<Return>', self.onEnter)
        self.bind('<BackSpace>', self.onBackspace)
        self.bind('<FocusIn>', self.onFocus)
        self.bind('<Tab>', self.onTab)
        self.bind('a', self.onA)
        self.bind('<Up>', self.onUp)
        self.bind('<Down>', self.onDown)
        
    def onUp(self, event):
        if self.historyIndex < (len(self.history)-1):
            
            # save what we have typed if we are leaving upwards
            if self.historyIndex == 0:
                self.addHistory()
            
            self.historyIndex = self.historyIndex+1
            self.setText(self.history[self.historyIndex])
            self.selectAll()
    
    def onDown(self, event):
        if self.historyIndex > 0:
            self.historyIndex = self.historyIndex-1
            self.setText(self.history[self.historyIndex])
            self.selectAll()
        
    def onA(self, event):
        """
        Select all with crtl+a
        """
        if event.state == 4:
            self.selectAll()
            return "break"

    def onTab(self, event):
        self.deleteSelection()
        self.insert(INSERT, '\t')
        
        return "break"

    def onFocus(self, event):
        
        self.xview(END)
        
        # select the whole line
        if not self.selection_present():
            self.selectAll()
        
    def onBackspace(self, event):
        """
        TODO: deleting words with crtl+backspace
        """
        
        if event.state == 4:
            return "break"
        
    def onEnter(self, event):
        
        self.announceInput(self.get())
        self.selection_range(0,END)
        
        self.addHistory()
        self.historyIndex = 0
        
    
    def addHistory(self):
        """
        If the command was repeated, or blank, do not add.
        Pop the last string if the queue is full.
        Then add the new one to front.
        """
        
        data = self.get()
        
        if data == '':
            return
        elif len(self.history) != 0 and self.history[0] == data:
            return
        
        if len(self.history) == self.historySize:
            self.history.pop()
            
        self.history.insert(0, data)
    
    def setText(self, text):
        self.delete(0, END)
        self.insert(0, text)
    
    def selectAll(self):
        self.selection_range(0,END)
    
    def deleteSelection(self):
        a,b = self.getSelectIndex()
        self.delete(a,b)
    
    def getSelectIndex(self):
        a = self.index(ANCHOR)
        b = self.index(INSERT)
        
        return (min(a,b), max(a,b))
    
    def announceInput(self, txt):
        """
        Send the message to all the queues. Split the message up
        by newlines
        """
        
        txt = txt.split('\n')
        
        for line in txt:
            
            for func in self.alertFuncs:
                func(line)
            
            for queue in self.alert:
                queue.put(line)
        
        
    
    def callOnInput(self, func):
        """
        When the user sends input, func will be called with the data.
        """
        
        self.alertFuncs.append(func)
        
    def raw_input(self, prompt=''):
        """
        Replacement for raw_input. This returns a new function that
        returns input sent from the box with an enter key.
        
        Currently blocking.
        TODO: somehow carry prompt info?
        """
        
        newQueue = Queue()
        
        self.alert.append(newQueue)
        
        def requestItem(prompt=''):
            out = newQueue.get()
            return out
        
        return requestItem