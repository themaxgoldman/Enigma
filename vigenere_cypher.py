from caesar_cypher import CaesarCypher
from cypher import Cypher

class VigenereCypher(Cypher):
    def __init__(self, key: str):
        if type(key) is not str or len(key) == 0:
            raise ValueError("Invalid key")

        self.cyphers = [CaesarCypher(letter) for letter in key]
        self.len_key = len(key)


    def encrypt(self, message: str) -> str:
        return ''.join([self.cyphers[(i % self.len_key)].encrypt(letter) for i,letter in enumerate(message)])


    def decrypt(self, message: str) -> str:
        return ''.join([self.cyphers[(i % self.len_key)].decrypt(letter) for i,letter in enumerate(message)])