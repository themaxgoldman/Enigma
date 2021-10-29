from cypher import Cypher
from typing import List, Tuple
from abc import ABC, abstractmethod


class EnigmaComponent(ABC):
    """
    Abstract enigma component with common methods
    """

    @abstractmethod
    def encode(self, letter: str, reverse: bool) -> str:
        """
        Encodes the letter

        Args:
            letter (str): the letter to encode
            reverse (bool): if the signal has already been reflected through the enigma

        Returns:
            str: the component's encoding of the input
        """

        pass


class _Plugboard(EnigmaComponent):
    """
    The plugboard enables swapping of pairs of letters and is the first component in the enigma
    """

    def __init__(self, plugboard_string: str):
        """
        Args:
            plugboard_string (str): a string representation of the plugboard, encoded as a sequence of 'X/Y' pairs
            separated by spaces (e.g. 'a/b c/d e/f g/h i/j')
        """

        self.plugboard = self.__from_string(plugboard_string)

    def __from_string(self, plugboard_string: str) -> str:
        plugboard = {}

        try:
            for swap in plugboard_string.lower().split():
                swap_letters = swap.split('/')
                plugboard[swap_letters[0]] = swap_letters[1]
                plugboard[swap_letters[1]] = swap_letters[0]
        except Exception as e:
            raise ValueError(f"Invalid plugboard string - {plugboard_string}", e)

        return plugboard

    def encode(self, letter: str, reverse: bool = False) -> str:
        return self.plugboard[letter] if letter in self.plugboard else letter


class _Rotor(EnigmaComponent):
    """
    The rotors, which sit between the plugboard and the reflector, scramble the letters according to their alphabet and
    current position. The rotors shift position after some fixed number of encodings as determined by their "speed",
    with the first rotor shifting after every encoding, the second rotor shifting once the first rotor has completed a
    full rotation, and so on
    """

    def __init__(self, rotor_string: str, speed: int):
        """
        Args:
            rotor_string (str): a string representation of the rotor, encoded as a permutation of the alphabet followed
            by its initial position (e.g. 'zxcvbnmasdfghjklqwertyuiop, 5')
            speed (int): the number of encodings before the rotor is shifted
        """

        self.rotor, self.pos = self.__from_string(rotor_string.lower())
        self.speed = speed
        self.count = 0

    def __from_string(self, rotor_string: str) -> Tuple[str, int]:
        try:
            rotor, pos = rotor_string.split(',')

            if len(rotor) != 26 or len(set(rotor)) != 26 or not rotor.isalpha():
                raise ValueError("Rotor string is not a valid permutation of the alphabet")

            return rotor, int(pos)
        except Exception as e:
            raise ValueError(f"Invalid rotor string - {rotor_string}", e)

    def encode(self, letter: str, reverse: bool = False) -> str:
        if (not letter.isalpha()):
            return letter

        if not reverse:
            self.count += 1
            if (self.count == self.speed):
                self.pos = (self.pos + 1) % 26
                self.count = 0

            offset = ord(letter) - ord('a')
            encoded_letter = self.rotor[(self.pos + offset) % 26]
        else:
            offset = ord(letter) - ord('a')
            idx = (self.rotor.index(letter) - self.pos) % 26
            encoded_letter = chr(idx + ord('a'))

        return encoded_letter


class _Reflector(EnigmaComponent):
    """
    The reflector reflects the signal from the rotors back through the machine and encodes letters such that
    encoding(k) = v iff encoding(v) = k
    """

    def __init__(self, reflector_string: str):
        """
        Args:
            reflector_string (str): a string representation of the reflector, encoded as a permutation of the
            alphabet p such that p[ord(k)] = v iff p[ord(v)] == k (e.g. 'badcfehgjilknmporqtsvuxwzy')
        """

        self.reflector = self.__from_string(reflector_string)

    def __from_string(self, reflector_string: str) -> str:
        try:
            if len(reflector_string) != 26 or len(set(reflector_string)) != 26 or not reflector_string.isalpha():
                raise ValueError("Reflector string is not a valid permutation of the alphabet")

            reflector = {chr(i + ord('a')): reflector_string[i] for i in range(26)}

            for k, v in reflector.items():
                if reflector[v] != k:
                    raise ValueError("Substitution must be symmetrical")

            return reflector
        except Exception as e:
            raise ValueError(f"Invalid reflector string - {reflector_string}", e)

    def encode(self, letter: str, reverse: bool = False) -> str:
        if (not letter.isalpha()):
            return letter

        return self.reflector[letter]


class Enigma(Cypher):
    """
    The engima machine, consisting of a plugboard, 1 or more rotors, and a reflector
    """

    def __init__(self, enigma_string: str):
        """
        Args:
            enigma_string (str): a string representation of the enigma, encoded as a plugboard string,
            followed by 1 or more rotor strings, followed by a reflector string
        """

        self.plugboard, self.rotors, self.reflector = self.__from_string(enigma_string)
        self.components = [self.plugboard] + self.rotors + [self.reflector]

    def __from_string(self, enigma_string: str) -> List[EnigmaComponent]:
        component_strings = enigma_string.lower().split('\n')
        try:
            plugboard = _Plugboard(component_strings[0])
            rotors = [_Rotor(component_strings[i], 26**(i-1)) for i in range(1, len(component_strings) - 1)]
            reflector = _Reflector(component_strings[-1])
        except Exception as e:
            raise ValueError(f"Invalid enigma configuration - {enigma_string}", e)

        return plugboard, rotors, reflector

    def encrypt(self, message: str) -> str:
        return ''.join([self.__encrypt_letter(letter) for letter in message.lower()])

    def __encrypt_letter(self, letter: str) -> str:
        for component in self.components:
            letter = component.encode(letter)

        for component in reversed(self.components):
            letter = component.encode(letter, reverse=True)

        return letter

    def decrypt(self, message: str) -> str:
        return self.encrypt(message)