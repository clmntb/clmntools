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
        self.filename = "out.png"
        return self.image
        
    def save(self,filename):
        extension = filename.split(".")[1]
        self.image.format = extension
        self.image.save(filename)
    
    def getLSB(self, mask=None):
        if not mask:
            mask = 0x1
        if not self.pixels:
            print "You need first to load an image!"
            return False
        self.lsb = []
        for y in range(self.height):
            self.lsb.append([])
            for x in range(self.width):
                pixel = self.pixels[x,y]
                self.lsb[-1].append( (  pixel[0] & mask , pixel[1] & mask , pixel[2] & mask ) ) 
    
    def readLSB(self, direction=None, mask=None):
        if not direction:
            direction = "GDHB"
        if not mask:
            mask = [(0,1,2)]
        
        index = 0
        result = ""
        
        if direction in ["GDHB","DGBH"]:
            for y in range(self.height):
                for x in range(self.width):
                    m = mask[index % len(mask)]
                    result += "".join( str(self.lsb[y][x][i]) for i in m if i!=-1 )
                    index+=1
        
        if direction in ["HBGD","BHDG"]:
            for x in range(self.width):
                for y in range(self.height):
                    m = mask[index % len(mask)]
                    result += "".join( str(self.lsb[y][x][i]) for i in m if i!=-1 )
                    index+=1
        
        if direction in ["DGBH","BHDG"]:
            result = result[::-1]
            
        return result
        
    def extract_colours(self):
        if not self.pixels:
            print "You need first to load an image!"
            return False
        self.colours = {}
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.pixels[x,y]
                if repr(pixel) not in self.colours.keys():
                    self.colours[repr(pixel)] = {}
                    self.colours[repr(pixel)]["nb"] = 1
                    self.colours[repr(pixel)]["position"] = len(self.colours.keys())
                else:
                    self.colours[repr(pixel)]["nb"] += 1
    
    def convert(self,extension):
        f = self.filename.split(".")[0]
        self.save(f+"."+extension)
    
    def info(self):
        print
        print "---Image properties---"
        print "Format: %s, Size: %dx%d, Mode: %s" % (self.image.format, self.width, self.height, self.image.mode)
        print 