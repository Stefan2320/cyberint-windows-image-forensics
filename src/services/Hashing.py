import hashlib
from src.models.Hash import Hasher


class MD5Hasher(Hasher):
    def compute_hash(self, path: str) -> str:
        with open(path,"rb") as f:
            return hashlib.md5(f.read()).hexdigest()