import Image
import StringIO
import sys,os

from Debuger import *

class Imager():
    def __init__(self,filename=None):
        self.image = None
        self.filename = filename
        if self.filename:
            self.open(self.filename)
    
    def open(self,filename):
        self.filename = filename
        self.image = Image.open(filename)
        self.image = self.image.convert("RGB")
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.pixels = self.image.load()
        return self.image
    
    def loadFromString(self,s):
        buff = StringIO.StringIO()
        buff.write(s)
        buff.seek(0)
        self.image = Image.open(buff)
        self.image = self.image.convert("RGB")
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.pixels = self.image.load()
        self.filename = "out." + self.image.format
        return self.image
        
    def save(self,filename):
        extension = filename.split(".")[1]
        self.image.format = extension
        self.image.save(filename)
    
    def getLSB(self):
        if not self.pixels:
            print "You need first to load an image!"
            return False
        self.lsb = []
        for y in range(self.height):
            self.lsb.append([])
            for x in range(self.width):
                pixel = self.pixels[x,y]
                self.lsb[-1].append( (  pixel[0] & 0x1 , pixel[1] & 0x1 , pixel[2] & 0x1 ) ) 
    
    def convert(self,extension):
        f = self.filename.split(".")[0]
        self.save(f+"."+extension)
    
    def info(self):
        print
        print "---Image properties---"
        print "Format: %s, Size: %dx%d, Mode: %s" % (self.image.format, self.width, self.height, self.image.mode)
        print 