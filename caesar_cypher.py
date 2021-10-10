class CaesarCypher:
    def __init__(self, key:str):
        if type(key) is not str or len(key) is not 1:
            raise ValueError("Invalid key")

        self.ALPHABET_LENGTH = 26
        self.ALPHA_OFFSET = ord('a')
        self.encrypt_offset = ord(key) - self.ALPHA_OFFSET
        self.decrypt_offset = -self.encrypt_offset


    def encrypt(self, message:str) -> str:
        return self.__encrypt_message(message, self.encrypt_offset)

    
    def decrypt(self, message:str) -> str:
        return self.__encrypt_message(message, self.decrypt_offset) 


    def __encrypt_message(self, message: str, offset:int) -> str:
        message = self.__normalize_message(message)
        return ''.join([self.__encrypt_letter(letter, offset) for letter in message])


    def __encrypt_letter(self, letter:str, offset:int) -> str:
        return chr(((ord(letter) + offset - self.ALPHA_OFFSET) % self.ALPHABET_LENGTH) + self.ALPHA_OFFSET) if letter.isalpha() else letter


    def __normalize_message(self, message:str) -> str:
        return message.lower()

    