import urllib,httplib,urllib2,base64
import socket
import hashlib
import fractions
import signal
import sys
from colorama import init,Fore, Back, Style
import traceback

DEBUG = 3
WARNING = 2
ERROR = 1
LOG_LEVEL = DEBUG

class Colors():
    def __init__(self):
        init(autoreset=True)
        self.HEADER = Fore.MAGENTA
        self.OK = Fore.BLUE
        self.DBG = Fore.GREEN
        self.WARNING = Fore.YELLOW
        self.ERROR = Fore.RED
        
    def color(self,s,c):
        if c == DEBUG:
            return self.DBG+"[DEBUG] "+s
        if c == WARNING:
            return self.WARNING+"[WARNING] "+s
        if c == ERROR:
            return self.ERROR+"[ERROR] "+s
        else:
            return s
        
class Debuger():
    def __init__(self,debug=LOG_LEVEL):
        self.count = 0
        self.max = 10
        self.signal = None
        self.dbg_level = debug
        self.colors = Colors()
        self.handles = []
    
    def setLevel(self,level):
        self.dbg_level = level
        if level == 3:
            self.log('Debug level changed to DEBUG',DEBUG)
    
    def handler(self,signum, frame):
        print 'Signal handler called with signal', signum
        self.count += 1
        self.log('Signal called %d time, %d remaining before quit' % (self.count, self.max-self.count),DEBUG)
        for handle in self.handles:
            handle.__call__()        
        if self.count == self.max:
            print self.log('Now Quitting...',DEBUG)
            sys.exit()

    def debug(self):
        self.object = object
        self.signal = signal.signal(signal.SIGINT, self.handler)
        self.log("The debuger is started, press CTRL+C to see traces",DEBUG)

    def add_handle(self,h):
        if not hasattr(h, '__call__'):
            self.log("The handle must be a function !", ERROR)
        else:
            self.handles.append(h)
            self.log("The handle has been successfuly registered",DEBUG)
        
    def log(self,log,level=DEBUG):
        if level <= self.dbg_level:
            print self.colors.color(log,level)

class Hasher():
    def md5(self,word):
        m = hashlib.md5()
        m.update(word)
        return m.hexdigest()
    def sha1(self,word):
        m = hashlib.sha1()
        m.update(word)
        return m.hexdigest()

class Mathor():
    def extended_gcd(self,aa, bb):
        lastremainder, remainder = abs(aa), abs(bb)
        x, lastx, y, lasty = 0, 1, 1, 0
        while remainder:
            lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
            x, lastx = lastx - quotient*x, x
            y, lasty = lasty - quotient*y, y
        return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

    def modinv(self, a, m):
        g, x, y = self.extended_gcd(a, m) 
        if g != 1:
            return None
        else:
            return x % m

    def gcd(self,a,b):
        return fractions.gcd(a, b)
        
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
        print colors().color("[DEBUG] Generator currently at %s" % self.current,colors().DBG)

 
class Browser():
    def __init__(self):
        self.opener = urllib2.build_opener()
        self.setCustomHeader("User-Agent","Mozilla/5.0 (Windows NT x.y; WOW64; rv:10.0) Gecko/20100101 Firefox/10.0")
    
    # def setDebugLevel(self,d):
        # handler=urllib2.HTTPHandler(debuglevel=d)
        # self.opener = urllib2.build_opener(handler)
        # self.setCustomHeader("User-Agent","Mozilla/5.0 (Windows NT x.y; WOW64; rv:10.0) Gecko/20100101 Firefox/10.0")
    
    def request(self,url,postdata=None):
        page = ""
        try:
            page = self.opener.open(url,postdata)
        except urllib2.HTTPError, e:
            Debuger().log('HTTPError = ' + str(e.code), ERROR)
        except urllib2.URLError, e:
            Debuger().log('URLError = ' + str(e.reason), ERROR)
        except httplib.HTTPException, e:
            Debuger().log('HTTPException', ERROR)
        except Exception:
            Debuger().log('generic exception: ' + traceback.format_exc(), ERROR)
        finally:
            return page.read()
    
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
            print "Connection error"
    
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
        import socks
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, host, port)
        self.socket = socks.socksocket()
        self.socket.settimeout(5)

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
        