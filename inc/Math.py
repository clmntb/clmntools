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
