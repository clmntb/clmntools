import urllib2,base64
import socket
import hashlib

class Hasher():
	def md5(self,word):
		m = hashlib.md5()
		m.update(word)
		return m.hexdigest()
	def sha1(self,word):
		m = hashlib.sha1()
		m.update(word)
		return m.hexdigest()

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

class Browser():
	def __init__(self):
		self.opener = urllib2.build_opener()
		self.setCustomHeader("User-Agent","Mozilla/5.0 (Windows NT x.y; WOW64; rv:10.0) Gecko/20100101 Firefox/10.0")
	
	def get(self,url):
		page = self.opener.open(url)
		return page.read()
	
	def post(self,url,postdata=""):
		page = self.opener.open(url,postdata)
		return page.read()
	
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
	
	def startServer(self):
		self.socket.bind((self.host, self.port))
		self.socket.listen(1)
		self.conn, self.addr = self.socket.accept()
		print 'Connected by', self.addr
		while 1:
			data = self.conn.recv(1024)
			print data
	
	def stopServer(self):
		self.conn.close()
	
	def sendData(self,data):
		self.socket.connect((self.host, self.port))
		self.socket.sendall(data)
	
	def receiveData(self):
		try:
			self.socket.connect((self.host, self.port))
			data = self.socket.recv(1024)
			print 'Received: ', repr(data)
		except:
			data = self.socket.recv(1024)
			print 'Received: ', repr(data)
	
	def setProxy(self,host,port):
		import socks
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, host, port)
		self.socket = socks.socksocket()

class Charsets():
	def __init__(self):
		self.majuscules = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		self.minuscules = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()
		self.digits = "0123456789"
		self.alphanumeric = self.digits + self.minuscules + self.majuscules  
		self.alpha = self.majuscules + self.minuscules
		self.all = "".join(chr(x) for x in range(0x20,ord("z") + 2))
		self.hexadecimal = self.digits + "abcdef"
		
class Decoder():
	def b64encode(self, string):
		return base64.b64encode(string)
	
	def b64decode(self, string):
		return base64.b64decode(string)
	
	def hexencode(self,string):
		s = ""
		for i in string:
			s += str(hex(ord(i))[2:])
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
		