from abc import ABC, abstractmethod

class Hasher(ABC):
    """
    An abstract base class for computing file hashes.

    Subclasses must implement the following methods:
        - compute_hash: Method to compute a hash for a given file path.
        - get_hash_type: Method to return the type of hash being computed.
    """

    @abstractmethod
    def compute_hash(self, path: str) -> str:
        """
        Computes the hash of a file located at the given path.

        Args:
            path (str): The file path for which to compute the hash.

        Returns:
            str: The computed hash of the file.
        """
        pass

    @abstractmethod
    def get_hash_type(self) -> str:
        """
        Returns the type of hash that this hasher computes.

        Returns:
            str: A string representing the type of hash (e.g., 'md5', 'sha256').
        """
        pass
