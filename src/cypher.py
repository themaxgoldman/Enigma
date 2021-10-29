from abc import ABC, abstractmethod

class Cypher(ABC):
    """
    Abstract cypher class with common methods
    """

    @abstractmethod
    def encrypt(self, message: str) -> str:
        """
        Encrypts the message using the designated algorithm and key

        Args:
            message (str): the message to encrypt

        Returns:
            str: the encrypted message
        """        
        pass

    @abstractmethod
    def decrypt(self, message: str) -> str:
        """
        Decrypts the message using the designated algorithm and key

        Args:
            message (str): the message to decrypt

        Returns:
            str: the decrypted message
        """        
        pass
    
