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
