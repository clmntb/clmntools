import urllib
import base64

class Generator():
    def __init__(self,minimal_len=None,charset="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
        self.charset = charset
        self.current = charset[0]
        self.len_min = minimal_len
        if self.len_min:
            self.current = charset[0]*self.len_min
    
    def update(self,mot):
        taille = len(mot)
        if mot == self.charset[-1]:
            return self.charset[0]*2
        if mot[taille-1] != self.charset[-1]:
            tmp = [x for x in mot]
            tmp[taille-1] = self.charset[self.charset.index(tmp[taille-1]) + 1]
            return"".join(tmp)
        else:
            return self.update(mot[:len(mot)-1]) + self.charset[0]
    
    def next(self):
        self.current = self.update(self.current)

    def debug(self):
        Debuger().log("Generator currently at %s" % self.current,DEBUG)


class Charsets():
    def __init__(self):
        self.majuscules = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.minuscules = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()
        self.digits = "0123456789"
        self.alphanumeric = self.digits + self.minuscules + self.majuscules  
        self.alpha = self.majuscules + self.minuscules
        self.all = "".join(chr(x) for x in range(0x20,ord("z") + 2)) + "\r\n"
        self.hexadecimal = self.digits + "abcdef"

class Decoder():
    def urlencode(self, string):
        s = ""
        for i in string:
            if i not in Charsets().minuscules and i not in Charsets().majuscules:
                zero = ""
                if len(hex(ord(i))[2:]) == 1: zero = "0"
                s += "%" + zero + hex(ord(i))[2:]
            else:
                s += i
        return s
    
    def urldecode(self, string):
        return urllib.urldecode(string)
    
    def b64encode(self, string):
        return base64.b64encode(string)
    
    def b64decode(self, string):
        return base64.b64decode(string)
    
    def hexencode(self,string):
        s = ""
        for i in string:
            zero = ""
            if len(hex(ord(i))[2:]) == 1: zero = "0"
            s += zero + hex(ord(i))[2:]
        return s
    
    def hexdecode(self,string):
        s = ""
        if (len(string) % 2) == 1:
            print "Error: The string length is even"
        for i in range(0,len(string),2):
            s += chr(int(string[i:i+2],16))
        return s
    
    def xor(self,string,key):
        s = ""
        for index,lettre in enumerate(string):
            s += chr( ord(lettre)^ord(key[index%len(key)]) )
        return s
    
    def base10toN(self,n, base, charset=None):
        if not charset:
            digits = "0123456789abcdefghijklmnopqrstuvwxyz"
        else:    
            digits = charset
        try:
            n = int(n)
            base = int(base)
        except:
            return ""

        if n < 0 or base < 2 or base > 36:
            return ""

        s = ""
        while 1:
            r = n % base
            s = digits[r] + s
            n = n / base
            if n == 0:
                break
        return s
    
    def baseNto10(self,n,base, charset=None):
        if not charset:
            digits = "0123456789abcdefghijklmnopqrstuvwxyz"
        else:    
            digits = charset
        try:
            base = int(base)
        except:
            print "Error 1"
            return
            
        if n < 0 or base < 2 or base > 36:
            print "Error 1"
            return
        
        n = n[::-1]
        r = 0
        for exposant,lettre in enumerate(n):
            r += digits.index(lettre)*(base**exposant)
        return r
    
    def baseNtoM(self,num,n,m, charset=None):
        if not charset:
            digits = "0123456789abcdefghijklmnopqrstuvwxyz"
        else:    
            digits = charset
        try:
            n = int(n)
            m = int(m)
        except:
            return
        
        if n < 2 or n > 36 or m < 2 or m > 36:
            return
        
        res = self.baseNto10(num,n,digits)
        res = self.base10toN(res,m,digits)
        return res
