import math
import random
import rsa

def gKey(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 2
    while (e < phi):
        if (math.gcd(e, phi) == 1):
            break
        else:
            e += 1
    d = (1 % phi) / e
    return e, n, d

def encrypt(m, e, n):
    c = pow(m, e)
    c = math.fmod(c, n)
    return c

def decrypt(c, d, n):
    m = pow(c, d)
    m = math.fmod(m, n)
    return m

def gSimple():
    num = random.randint(100000, 10000000)
    while not isPrime(num):
        num+=1
    return num

def isPrime(n):
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n and n % d != 0:
        d += 2
    return d * d > n
