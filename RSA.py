import random, string, re, os
from fractions import gcd

#for inverses
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
#end for inverses

def generate_public(): # used in generating public, as well as providing the private information
    primes = []

    for i in range(0, 2):
        primes.append(find_primes())

    m = primes[0] * primes[1]
    phi = (primes[0] - 1) * (primes[1] - 1)
    e = get_encryption(phi)
    d = get_decryption(e, phi)
    print("Your public key and modulus are: " + str((e, m)).replace('L', ''))
    print("Your Primes are: " + str((primes[0], primes[1])).replace('L', ''))
    print("Your private decryption: " + str(d).replace('L', ''))
    #print("phi(m): " + str(phi).replace('L', ''))

def get_decryption(e, phi): # used in generating private information
    return modinv(e, phi)

def find_primes(): # used in generating public information
    # The primes here are not very large, but this is more for fun than implementation.
    # This is the Miller-Rabin primality test. At 40 rounds, we can be fairly certain the number a is prime.
    # if you are not convinced of this, I suggest googling or working out the probability yourself.
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

def encrypt(m, e): #encrypts text using RSA and saves it as a txt file in the directory
    unencrypted = raw_input('Text to encrypt: ').lower()
    chars = re.escape(string.punctuation)
    unencrypted = re.sub(r'[' + chars + ']', '', unencrypted)
    message = []
    for letter in unencrypted:
        if letter.isdigit():
            raise Exception('You need to spell your numbers out. E.g. 8 -> eight')
        number = ord(letter) - 96
        if number == -64:
            number = 0
        message.append(number)
    for i in range(0, len(message)):
        message[i] = pow(message[i], e, m)

    file = open('RSA_Message.txt', 'w')
    file.write(str(message).replace('[','').replace(']','').replace('L','').replace(' ',''))
    file.close()
    return 'Your message was saved to ' + str(os.getcwd())

def decrypt(message, d, m): # takes the message to decrypt and decrypts it
    translate = dict(enumerate(string.ascii_lowercase, 1))
    for i in range(0, len(message)):
        message[i] = long(message[i])
        if message[i] == 0:
            message[i] = " "
        else:
            message[i] = translate[pow(message[i], d, m)]
    return str(''.join(message))

def message_to_decrypt(): # open a file with the RSA message, separated by commas
    from Tkinter import Tk
    from tkFileDialog import askopenfilename
    Tk().withdraw()
    file_path = askopenfilename()
    text_file = open(file_path, "r")
    message = text_file.read().split(',')
    text_file.close()
    return message
