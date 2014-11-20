import fractions

from Debuger import *

class Maths():
    def gcd(self,a,b):
        return fractions.gcd(a, b)

    def egcd(self,aa, bb):
        lastremainder, remainder = abs(aa), abs(bb)
        x, lastx, y, lasty = 0, 1, 1, 0
        while remainder:
            lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
            x, lastx = lastx - quotient*x, x
            y, lasty = lasty - quotient*y, y
        return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

    def modinv(self, a, m):
        g, x, y = self.egcd(a, m) 
        if g != 1:
            return None
        else:
            return x % m
    
    def invertible(self,matrix):
        """
        Return True if a 2*2 matrix is inversible in Z26.
        """
        determinant = matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
        return self.gcd(determinant, 26) == 1

    def inverse_matrix(self,matrix):
        """
        Inverse a 2*2 matrix.
        """
        if not self.invertible(matrix):
            return "Non invertible matrix"
        result = [i[:] for i in matrix]
        result[0][0] = matrix[1][1]
        result[1][1] = matrix[0][0]
        result[1][0] = (-matrix[1][0]) % 26
        result[0][1] = (-matrix[0][1]) % 26
        return result
        
    def isprime(self,n,m):
        if self.gcd(n,m) == 1:
            return True
        return False
    
class Analyzer():
    def __init__(self, ciphertext="", language="",nospace=False):
        self.ics = { "FR": 0.0778, "EN": 0.0667, "DE": 0.0762, "ES": 0.0770, "IT": 0.0738, "RU": 0.0529 }
        self.language = ""
        self.ciphertext = ""
        if language:
            self.setLanguage(language)
        if ciphertext:
            self.setCipherText(ciphertext,nospace)
        if not self.language:
            Debuger().log("Please note that no language has been defined yet, please use setLanguage", WARNING)
        if not self.ciphertext:
            Debuger().log("Please note that no ciphertext has been defined yet, please use setCipherText", WARNING)
    
    def setLanguage(self,language):
        if language in self.ics:
            self.language = language
        else:
            Debuger().log('%s is not an accepted languages : %s' % (language,self.ics.keys().__repr__()), ERROR)
    
    def setCipherText(self,ciphertext,nospace=False):
        if nospace: 
            self.ciphertext = ciphertext.replace(" ","")
        else:
            self.ciphertext = ciphertext
    
    def ic_compare(self,delta=0.001):
        if not self.language:
            Debuger().log('A language must be set to call this function', ERROR)
        else:
            if self.ic <= (self.ics[self.language] + delta) and self.ic >= (self.ics[self.language] - delta):
                # Debuger().log('IC = %s' % str(self.ic), DEBUG)
                return True
        return False
    
    def ic_calc(self, b_len=1):
        self.frequency(b_len)
        self.ic = 0
        l = len(self.ciphertext)
        for f in self.freqs.values(): 
            self.ic += float(f*(f-1))/(l*(l-1))
        # Debuger().log('Index of coincidence : %s' % str(self.ic), DEBUG)
    
    def frequency(self,b_len=1):
        self.freqs = {}
        self.nb_lettres = 0
        if (len(self.ciphertext) % b_len) != 0:
            Debuger().log('The block length should be a divisor of the length of the ciphertext. (len(c)=%d, b_len=%d' % (len(self.ciphertext),b_len), DEBUG)

        for i in range(0,len(self.ciphertext)-b_len+1):
            try:
                tmp = self.ciphertext[i:i+b_len]
                if tmp in self.freqs:
                    self.freqs[tmp] += 1
                else:
                    self.freqs[tmp] = 1
                self.nb_lettres += 1
            except:
                pass
        # Debuger().log('Frequencies for a block length of %d\n%s' % (b_len,self.freqs.__repr__()),DEBUG)
        return True