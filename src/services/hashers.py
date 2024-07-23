import hashlib
from src.utils.abstract_hasher import Hasher


class MD5Hasher(Hasher):
    def compute_hash(self, path: str) -> str:
        """
        Computes the MD5 hash of the file specified by the given path.
        """
        with open(path, "rb") as file:
            return hashlib.md5(file.read()).hexdigest()

    def get_hash_type(self) -> str:
        """
        Returns the hash type ("MD5") used by this hasher.
        """
        return "MD5"


class SHA1Hasher(Hasher):
    def compute_hash(self, path: str) -> str:
        """
        Computes the SHA-1 hash of the file specified by the given path.
        """
        with open(path, "rb") as file:
            return hashlib.sha1(file.read()).hexdigest()

    def get_hash_type(self) -> str:
        """
        Returns the hash type ("SHA1") used by this hasher.
        """
        return "SHA1"
