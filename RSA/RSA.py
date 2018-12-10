import random, string, re, os
from fractions import gcd
from nltk import tokenize


class RSAProgram:

    def __init__(self, e=None, m=None, p1=None, p2=None, d=None):
        asarray = [e,m,p1,p2,d]
        if any(t is None for t in asarray):
            info = generate_public()
            print("Default values filled, you were missing an argument")
            self.encrypt = info[0]
            self.modulus = info[1]
            self.prime1 = info[2]
            self.prime2 = info[3]
            self.decrypt = info[4]
        else:
            self.encrypt = e
            self.modulus = m
            self.prime1 = p1
            self.prime2 = p2
            self.decrypt = d


#### Find Inverses ####
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
########################


def generate_public(): # used in generating public, as well as providing the private information
    primes = []

    for i in range(0, 2):
        primes.append(find_primes())

    m = primes[0] * primes[1]
    phi = (primes[0] - 1) * (primes[1] - 1)
    e = get_encryption(phi)
    d = get_decryption(e, phi)
    return [e, m, primes[0], primes[1], d]


def get_decryption(e, phi): # used in generating private information
    return modinv(e, phi)


def find_primes(): # used in generating public information
    # The primes here are not very large, but this is more for fun than implementation.
    # This is the Miller-Rabin primality test. At 40 rounds, we can be fairly certain the number a is prime.
    # if you are not convinced of this, I suggest something-searching or working out the probability yourself.
    a = random.randint(2 ** 32, 2 ** 64)
    while pow(2, a - 1, a) != 1:
        while (a % 2) == 0:
            a = random.randint(2 ** 32, 2 ** 64)
        for i in range(1,50):
            if pow(i, a, a) != i:
                a = random.randint(2 ** 32, 2 ** 64)
                break
    return a


def get_encryption(b): # used in generating public information
    a = random.randint(4, b)
    while gcd(a, b) != 1:
        a = random.randint(4, b)
    return a


def encrypt(m, e): #encrypts text using RSA and returns the message as list
    unencrypted = raw_input('Text to encrypt: ').lower()
    chars = re.escape(string.punctuation)
    unencrypted = re.sub(r'[' + chars + ']', '', unencrypted)
    message = []

    for tokens in tokenize.sent_tokenize(unencrypted):
        for letter in tokens:
            if letter.isdigit():
                raise Exception('You need to spell your numbers out (e.g. 8 -> eight)')
            number = ord(letter) - 96
            if number == -64:
                number = 0
            message.append(number)
        for i in range(0, len(message)):
            if message[i] != 0:
                message[i] = pow(message[i], e, m)
    return(message)


def decrypt(message, d, m): # takes the message to decrypt and decrypts it
    translate = dict(enumerate(string.ascii_lowercase, 1))
    to_return = []
    for letter in message:
        if letter == 0:
            to_return.append(" ")
        else:
            to_return.append(translate[pow(letter, d, m)])
    return str(''.join(to_return))


def message_to_decrypt(): # open a file with the RSA message, separated by commas
    from Tkinter import Tk
    from tkFileDialog import askopenfilename
    Tk().withdraw()
    file_path = askopenfilename()
    text_file = open(file_path, "r")
    message = text_file.read().split(',')
    text_file.close()
    return message
