from Tkinter import *
import threading
import time


def dispatch(method):
    """
    Decorator for making Tkinter methods multithread safe.
    This is needed whenever an outside thread executes Tkinter commands.
    
    It works by postponing execution until ready.
    """
    
    def wrapper(self, *args, **kw):
        self.after_idle(method, self, *args, **kw)
    
    return wrapper



class TextBox(Text, object):
    """
    Special Text widget. 
    """
    lines = 500
    collect = ''
    
    def __init__(self, master=None, cnf={}, **kw):
        # Create the Text widget with vertical scrollbar widget
        Text.__init__(self, master, cnf, **kw)
        self.scrollY = Scrollbar(master, orient=VERTICAL)
        
        # Connect the widgets
        self.config(yscrollcommand=self.scrollY.set)            
        self.scrollY.config(command=self.yview)
        
        self.scrollY.bind('<ButtonRelease-1>', self.onScroll)
        
        self.poll()

    def onScroll(self, event):
        self.scrollY.focus_set()
      
    def grid(self, **kw):
        # position the TextBox and the scrollbar right beside it
        super(TextBox, self).grid(**kw)
        self.scrollY.grid(row=kw['row'], column=kw['column']+1, sticky=N+S)

    def deleteAll(self):
        self.delete(1.0, END)
        
    def editable(self):
        """
        Returns
        "normal" - User can edit the box
        "disabled" - User cannot edit the box
        """
        return self.cget('state')
        
    
    def scrolledDown(self):
        # save scrollbar position
        if float(self.scrollY.get()[1]) == 1.0:
            return True
        return False
            
    
    
    # Updating the screen.
    # Here we setup a buffer, so the textbox doesn't have to be redrawn every
    # time there is a text update. If you update too fast, it can crash the UI.
    # The method poll updates the collected data every couple of milliseconds.
    #
    # TODO: optimize this area, and perhaps cut lines that are too long.
    
    def poll(self):
        if self.collect != []:
            self.write2(getLastLines(''.join(self.collect), self.lines))
            self.collect = []
            
        self.after(100, self.poll)
        
    #@dispatch
    def write(self, rawstring):
        self.collect.append(rawstring)
    
    def write2(self, rawstring):
        """
        Write a string into the box.
        Note: Each call takes 0.0025 seconds on 1.20 ghz
        
        TODO: Maybe faster to keep track of size by counting newlines.
        """

        # save the old edit state and enable edits
        oldstate = self.editable()
        self.config(state=NORMAL)
        
        # insert the string
        self.insert(END, rawstring)
        
        # delete lines if overflow
        #size = float(self.index(END))
        #if size > self.lines:
        #   self.delete( '1.0', '%s.0' % int(size-self.lines+1) )
        
        # reset the edit state
        if oldstate == 'disabled':
            self.config(state=DISABLED)
        
        
        # scroll to the bottom if the scrollbar was at the bottom
        if self.scrolledDown():
            self.yview_moveto(1.0)
            #self.see(END)
            


def getLastLines(haystack, num):
    num += 1
    split = haystack.rsplit('\n', num)
    if len(split) > num:
        return '\n'.join(split[1:])
    return haystack