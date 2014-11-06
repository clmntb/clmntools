import hashlib 
import hmac

class Hasher():
    def md5(self,word):
        return hashlib.md5(word).hexdigest()

    def sha1(self,word):
        return hashlib.sha1(word).hexdigest()
        
    def sha224(self,word):
        return hashlib.sha224(word).hexdigest()

    def sha256(self,word):
        return hashlib.sha256(word).hexdigest()

    def sha384(self,word):
        return hashlib.sha384(word).hexdigest()

    def sha512(self,word):
        return hashlib.sha512(word).hexdigest()

    def ripemd160(self,word):
        m = hashlib.new('ripemd160')
        m.update(word)
        return m.hexdigest()    
    
    def hmacMD5(self,word,salt):
        return hmac.new(salt, msg=word, digestmod=hashlib.md5).hexdigest()

    def hmacSHA1(self,word,salt):
        return hmac.new(salt, msg=word, digestmod=hashlib.sha1).hexdigest()

    def hmacSHA224(self,word,salt):
        return hmac.new(salt, msg=word, digestmod=hashlib.sha224).hexdigest()

    def hmacSHA256(self,word,salt):
        return hmac.new(salt, msg=word, digestmod=hashlib.sha256).hexdigest()

    def hmacSHA384(self,word,salt):
        return hmac.new(salt, msg=word, digestmod=hashlib.sha384).hexdigest()

    def hmacSHA512(self,word,salt):
        return hmac.new(salt, msg=word, digestmod=hashlib.sha512).hexdigest()

    def hmacRIPMD160(self,word,salt):
        return hmac.new(salt, msg=word, digestmod=lambda: hashlib.new('ripemd160')).hexdigest()
    