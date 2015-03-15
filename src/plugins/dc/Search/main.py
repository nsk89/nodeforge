from nodeforge.PluginUtils import *
from threading import Thread

import urllib2, re, copy

class Main(Plugin):

    def onLoad(self):
        """
        Load the parser.
        """
        
        self.parse = self.core.findPlugin('NMDC Parser')
        self.googleLimit = 2


    def onData(self, txt):
        context = self.parse.context
        
        if context.cmd == '/google' or context.cmd == '/g':
            Thread(target=self.google, args=(copy.copy(context),) ).start()
        elif context.cmd == '/wp':
            Thread(target=self.google, args=(copy.copy(context),'site:en.wikipedia.org') ).start()
        elif context.cmd == '/calc':
            Thread(target=self.google, args=(copy.copy(context),'=',True) ).start()
        
    def google(self, context, append='', calc=False):

        term = context.args
        term += ' ' + append
        
        term = urllib2.quote(term)
        
        req = urllib2.Request('http://www.google.com/search?q=%s' % term)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9b3) Gecko/2008020514 Firefox/2.10')
        req.add_header('Ua-Cpu','x86')
        req.add_header('Accept','image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-ms-application, application/vnd.ms-xpsdocument, application/xaml+xml, application/x-ms-xbap, application/msword, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/x-shockwave-flash, */*')
        req.add_header('Accept-Language','en-us')
        
        res = urllib2.urlopen(req).read()
        res = res.replace('&#215;','*').replace('<sup>','^').replace('</sup>','')
        
        
        if calc:
            linkre = re.compile("size=\+1><b>(.*?)</b>")
        else:
            linkre = re.compile("class=r><a href=\"(http:\\/\\/.*?)\"")
        
        #print res
        
        links = linkre.findall(res)
        
        if links == []:
            context.reply("No results found")
        else:
            links[0] = re.compile('<.*?/?> <.*?/?>').sub('',links[0])
            try:
                msg = ''
                for i in xrange(self.googleLimit):
                    msg += links[i]+'  '
            except:
                pass
            finally:
                context.reply(msg)