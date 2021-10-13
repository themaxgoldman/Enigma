from cypher import Cypher

class Enigma(Cypher):

    # Plugboad - 6 letters are swapped (symmetric)
    # Rotor - fast, middle, slow
    # Reflector - swaps every letter (symmetric)

    def __init__(self, enigma_string : str):
        enigma_string_split = enigma_string.lower().split('\n')
        self.plugboard = Plugboard(enigma_string_split[0]) 
        speed_list = [1,26,26**2]
        self.rotors = [0,0,0]
        self.rotors[0] = Rotor(enigma_string_split[1], 26**0)
        self.rotors[1] = Rotor(enigma_string_split[2], 26**1)
        self.rotors[2] = Rotor(enigma_string_split[3], 26**2)
        self.reflector = Reflector(enigma_string_split[-1])
        

    def encrypt(self, message: str) -> str:
        return ''.join([self.__encrypt_letter(letter) for letter in message])

    def __encrypt_letter(self, letter : str) -> str:
        plugboard_encryption = self.plugboard.encode(letter)
        rotors_encryption = plugboard_encryption
        for i in range(len(self.rotors)):
            rotors_encryption = self.rotors[i].encode(rotors_encryption,direction='f')

        reflector_encryption = self.reflector.encode(rotors_encryption)
    
        rotors_encryption = reflector_encryption
        for i in reversed(range(len(self.rotors))):
            rotors_encryption = self.rotors[i].encode(rotors_encryption,direction='b')

        plugboard_encryption = self.plugboard.encode(rotors_encryption)

        return plugboard_encryption
        

    def decrypt(self, message: str) -> str:
        return self.encrypt(message)


    
class Plugboard:
    '''
    The plugboard is the first component used in the encryption.
    It allows letters to be swapped with other letters (symmetric) 
    '''
    def __init__(self, plugboard_string : str):
        self.plugboard = self.__from_string(plugboard_string)

    def __from_string(self, plugboard_string : str) -> str:
        plugboard = {}

        try:
            for swap in plugboard_string.lower().split():
                swap_letters = swap.split('/')
                plugboard[swap_letters[0]] = swap_letters[1]
                plugboard[swap_letters[1]] = swap_letters[0]
        except Exception as e:
            raise Exception("Invalid plugboard string", e)

        return plugboard
    
    def encode(self, letter : str) -> str:
        if letter in self.plugboard:
            return self.plugboard[letter]
        else:
            return letter
            

class Rotor:
    '''
    Rotors map an index [0,25] to an letter
    Depending on if the rotor is SLOW, MIDDLE, or FAST, the encoding will shift by 1 after a certain number of uses
    '''
    def __init__(self, rotor_string : str, speed : int):
        self.rotor,self.pos = self.__from_string(rotor_string.lower())
        self.pos = int(self.pos)
        self.speed = speed
        self.count = 0

    def __from_string(self, rotor_string : str):
        try:
            rotor,pos = rotor_string.split(',')

            if len(set(list(rotor))) != 26 or not rotor.isalpha():
                raise Exception()

            return rotor,pos
        except Exception as e:
            raise Exception("Invalid rotor string", e)

        
    def encode(self, letter : str, direction : str) -> str:
        if (not letter.isalpha()):
            return letter

        if direction == 'f':
            self.count = self.count + 1 
            if (self.count == self.speed):
                self.pos = (self.pos + 1) % 26
                self.count = 0

            letter = letter.lower()
            offset = ord(letter) - ord('a')
            encoded_letter = self.rotor[(self.pos + offset) % 26]
        else:
            letter = letter.lower()
            offset = ord(letter) - ord('a')
            idx = (self.rotor.index(letter) - self.pos) % 26
            encoded_letter = chr(idx + ord('a'))
        
        return encoded_letter
            
            
            

class Reflector:
    '''
    The reflector swaps each letter in the alphabet with another letter (symmetric)
    '''
    def __init__(self, reflector_string: str):
        self.reflector = self.__from__string(reflector_string)

    def __from__string(self, reflector_string: str) -> str:
        try:
            if len(set(list(reflector_string))) != 26 or not reflector_string.isalpha():
                raise Exception()
            
            reflector = {chr(n + ord('a')): reflector_string[n] for n in range(26)}

            for k,v in reflector.items():
                if reflector[v] != k:
                    raise Exception()
                    
            return reflector
        except Exception as e:
            raise ValueError("Invalid reflector string")
        
    def encode(self, letter: str) -> str:
        if (not letter.isalpha()):
            return letter
        letter = letter.lower()
        return  self.reflector[letter]
            


# Plugboard: a/b e/r t/y l/o p/f c/v
# Fast rotor, pos: zxcvbnmasdfghjklqwertyuiop, 5
# Middle rotor, pos: qwertyuiopasdfghjklzxcvbnm, 0
# Slow rotor, pos: qazwsxedcrfvtgbyhnujmikolp, 20
# Reflector: badcfehgjilknmporqtsvuxwzy

'''a/b e/r t/y l/o p/f c/v
zxcvbnmasdfghjklqwertyuiop,0
qwertyuiopasdfghjklzxcvbnm,0
qazwsxedcrfvtgbyhnujmikolp,0
badcfehgjilknmporqtsvuxwzy'''

if __name__ == '__main__':
    enigma_string = "a/b e/r t/y l/o p/f c/v\nzxcvbnmasdfghjklqwertyuiop,25\nqwertyuiopasdfghjklzxcvbnm,25\nqazwsxedcrfvtgbyhnujmikolp,25\nbadcfehgjilknmporqtsvuxwzy"
    enigma = Enigma(enigma_string)

    encrypt_target = 'hello my name is max goldman and I am super cool I hope this is more than twenty six letters'

    encrypted = enigma.encrypt(encrypt_target)

    enigma = Enigma(enigma_string)
    decrypted = enigma.encrypt(encrypted)
    print(decrypted)