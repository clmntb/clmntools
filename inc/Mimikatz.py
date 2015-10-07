import re

class Credential():
    def __init__(self):
        self.username = None
        self.domain = None
        self.password = None

    def setUsername(self,u):
        self.username = u

    def setPassword(self,p):
        self.password = p

    def setDomain(self,d):
        self.domain = d

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def getDomain(self):
        return self.domain

    def __repr__(self):
        return "Credential: %s\\%s : %s" % (self.domain,self.username,self.password)



class Mimikaz():
    def __init__(self):
        self.creds = []
        self.unique_passwords = []

    def cred_exists(self,cred):
        for c in self.creds:
#            if c.getUsername().lower() == cred.lower():
            if c.getUsername() == cred:
                return True
        return False

    def add_file(self,file):
        self.file = None
        with open(file,'r') as f:
            self.file = f.read()

    def parse(self):
        lines = self.file.split("\n")
        i = 0
        while i<len(lines):
            match = re.search("\*\sUsername\s:\s(.*?)\r",lines[i])
            if match:
                username = match.groups()[0]
                if username!="(null)" and not self.cred_exists(username):
                    tmp_cred = Credential()
                    tmp_cred.setUsername(username)
                    #self.creds.append({})
                    i+=1
                    match = re.search("\*\sDomain\s+:\s+(.*?)\r",lines[i])
                    if match:
                        domain = match.groups()[0]
                        tmp_cred.setDomain(domain)
                        i+=1
                        match = re.search("\*\sPassword\s+:\s(.*?)\r",lines[i])
                        if match:
                            password = match.groups()[0]
                            if password != "(null)" and not re.search("([a-fA-F0-9]{2}\s)+",password):
                                tmp_cred.setPassword(password)
                                if password not in self.unique_passwords:
                                    self.unique_passwords.append(password)
                                self.creds.append(tmp_cred)
            i+=1

    def printCreds(self):
        print "Number of credentials:", len(self.creds)
        print "Number of unique passwords:", len(self.unique_passwords)
        for c in self.creds:
            print c

    def exportWordlist(self,file):
        with open(file,"w") as f:
            for p in self.unique_passwords:
                f.write(p+"\n")



