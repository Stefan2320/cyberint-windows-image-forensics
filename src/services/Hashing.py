import hashlib
from src.models.Hash import Hasher


class MD5Hasher(Hasher):
    def compute_hash(self, path: str) -> str:
        with open(path,"rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def get_hash_type(self) -> str:
        return "MD5"

class SHA1Hasher(Hasher):
    def compute_hash(self, path: str) -> str:
        with open(path,"rb") as f:
            return hashlib.sha1(f.read()).hexdigest()
    
    def get_hash_type(self) -> str:
        return "SHA1"