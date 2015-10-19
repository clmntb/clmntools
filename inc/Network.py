import httplib
import urllib2
import socket
import socks
import traceback
import sys,os
import string
from ..vendor.irclib import irclib
from ..vendor.irclib import ircbot
from ..vendor.pytesser import pytesser
import math

try:
    from PIL import Image
except:
    import Image

import StringIO
import subprocess

from Debuger import *
from String import *

class Browser():
    def __init__(self, proxy=None, cookie=None):
        self.opener = urllib2.build_opener()
        self.setCustomHeader("User-Agent","Mozilla/5.0 (Windows NT x.y; WOW64; rv:10.0) Gecko/20100101 Firefox/10.0")
        if proxy:
            self.setProxy(proxy[0], proxy[1])
        if cookie:
            self.setCookie(cookie)
    
    # def setDebugLevel(self,d):
        # handler=urllib2.HTTPHandler(debuglevel=d)
        # self.opener = urllib2.build_opener(handler)
        # self.setCustomHeader("User-Agent","Mozilla/5.0 (Windows NT x.y; WOW64; rv:10.0) Gecko/20100101 Firefox/10.0")
    
    def request(self,url,postdata=None):
        page = ""
        try:
            page = self.opener.open(url,postdata)
            return page.read()
        except urllib2.HTTPError, e:
            Debuger().log('HTTPError = ' + str(e.code), ERROR)
        except urllib2.URLError, e:
            Debuger().log('URLError = ' + str(e.reason), ERROR)
        except httplib.HTTPException, e:
            Debuger().log('HTTPException', ERROR)
        except Exception:
            Debuger().log('generic exception: ' + traceback.format_exc(), ERROR)
    
    def get(self,url):
        return self.request(url)
    
    def post(self,url,postdata=""):
        return self.request(url,postdata)
    
    def setCookie(self,cookie):
        self.setCustomHeader('Cookie',cookie)
    
    def setCustomHeader(self,header,value):
        present = False
        if self.opener.addheaders != []:
            for h in self.opener.addheaders:
                if h[0] == header:
                    present = True
        if present: 
            headers = list()
            for h in self.opener.addheaders:    
                if h[0] == header:
                    headers.append((header,value))
                else:
                    headers.append((h[0],h[1]))
            self.opener.addheaders = headers
        else:
            self.opener.addheaders.append((header,value))
    
    def setProxy(self,url,port):
        proxy = urllib2.ProxyHandler({'http':url + ":" + str(port),'https':url + ":" + str(port)})
        self.opener = urllib2.build_opener(proxy)
        self.setCustomHeader("User-Agent","Mozilla/5.0 (Windows NT x.y; WOW64; rv:10.0) Gecko/20100101 Firefox/10.0")
    
    def basicAuthentication(self,username,password):
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        self.setCustomHeader("Authorization", "Basic %s" % base64string)   
        
class Socketer():
    def __init__(self,host="",port=6666):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.socket.settimeout(5)
    
    def setRemote(self,host,port):
        self.host=host
        self.port=port
    
    def startServer(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        self.conn, self.addr = self.socket.accept()
        print 'Connected by', self.addr
        while 1:
            data = self.conn.recv(4096)
            print data
    
    def close(self):
        self.socket.close()
    
    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            self.connected = True
        except:
            "Connection error"
            raise
    
    def send(self,data):
        if not self.connected: 
            self.connect()
        self.socket.sendall(data)
    
    def receive(self):
        if not self.connected: 
            self.connect()
        data = self.socket.recv(4096)
        return data
    
    def setProxy(self,host,port):
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, host, port)
        self.socket = socks.socksocket()
        self.socket.settimeout(5)


class IRCbot(ircbot.SingleServerIRCBot):
    def __init__(self,server,port,chan, proxy=None):
        ircbot.SingleServerIRCBot.__init__(self,[(server,port)], "clmntbot","bot by clmnt",proxy=proxy)
        self.chan=chan
        self.index = 1
        self.rapporter = False
        self.ircobj.add_global_handler("all_events", self.rapport)
        self.started = False
        
    def on_welcome(self, serv, ev):
        print ev.arguments()[0]
        if self.chan:
            serv.join(self.chan)
    
    def on_privnotice(self,serv,ev):
        print ev.arguments()[0]
    
    def on_pubnotice(self,serv,ev):
        print ev.arguments()[0]
        
    def on_join(self,serv,ev):
        if not self.started:
            print "%s successfuly joined" % self.chan
            serv.privmsg("Daneel",".challenge_xor_ocr start")
            self.started = True
        else:
            print "%s successfuly joined" % self.chan_rep 
            print "Sending ", self.rep
            serv.privmsg(self.chan_rep,self.rep)
            
    
    def on_pubmsg(self,serv,ev):
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0]        
        print "Message received - %s - %s : %s" % (auteur, canal, message)

    def rapport(self, serv, ev):
        if self.rapporter:
            print repr((ev.eventtype(), ev.source(), ev.target(), ev.arguments()))
 
        
    def on_privmsg(self,serv,ev):
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0]
        try:
            print "Message received - %s : %s" % (auteur, message)
        except:
            print repr((ev.eventtype(), ev.source(), ev.target(), ev.arguments()))

        
        image = Decoder().b64decode(message)
        
        header = Decoder().hexdecode("89504E470D0A1A0A0000000D49484452")
        
        key = ""
        for i in range(8):
            key += chr( ord(image[i]) ^ ord(header[i]) )
        
        print "Found key: ", key
        
        decoded_image = ""
        for i in range(len(image)):
            decoded_image += chr ( ord(image[i]) ^ ord(key[i%len(key)]) )
        
        buff = StringIO.StringIO()
        buff.write(decoded_image)
        buff.seek(0)
        im = Image.open(buff)
        im=im.rotate(90*3)
        rgb_im=im.convert("RGB")
        new_image = Image.new( 'RGB', im.size )
        pixels = new_image.load()
        
        for i in range(rgb_im.size[0]):
            for j in range(rgb_im.size[1]):
                pix = rgb_im.getpixel((i,j))
                if pix[0] == 0 and pix[1] == 0 and pix[2] == 0:
                    new_pix = (255,255,255)
                else:
                    new_pix = (0,0,0)
                pixels[i,j] = new_pix
        
        
        new_image.save("Test.png")
        
        lettres = []
        for i in range(12):
            lettre = Image.new( 'RGB', (8,10) )
            p = lettre.load()
            for a in range(0,8):
                for b in range(0,10):
                    p[a,b] = new_image.getpixel((a+1+i*8,b+4))
            lettres.append(lettre)
            lettre.save("lettre_"+str(i)+".png")
        
        img_string = ""
        for i,lettre in enumerate(lettres):
            pix = []
            for a in range(0,8):
                for b in range(0,10):
                    p = lettre.getpixel((a,b))
                    if p[0] == 0:
                        pix.append("0")
                    else:
                        pix.append("1")
            txt_rep = "-".join(pix)
            
            known = ""
            with open("config_lettres.txt","r") as f:
                known = f.readlines()
            
            ok = False
            for k in known:
                txt_known = k.strip().split(":")[1]
                if txt_rep == txt_known:
                    ok = True
                    current_lettre = k.strip().split(":")[0]
                    
            f.close()
            
            if not ok:
                current_lettre = raw_input('What is Image_%d.png ? ' % i)
                with open("config_lettres.txt","a") as f:
                    f.write(current_lettre + ":" + txt_rep +"\n")
            
            img_string += current_lettre
        
        print "OCR: ", img_string
        
        serv.join("#" + key)
        self.rep = ".challenge_xor_ocr " + img_string
        self.chan_rep = "#" + key
        
