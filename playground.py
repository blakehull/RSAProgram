from RSA import RSA as rsa

program = rsa.RSAProgram()
message = rsa.encrypt(program.modulus, program.encrypt)

print(message)

raw_input('press enter when ready to decrypt').lower()

print(rsa.decrypt(message, program.decrypt, program.modulus))
