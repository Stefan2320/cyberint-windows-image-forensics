class File:
    def __init__(self, hashes: dict = {}, path: str = None, is_malicious: bool = None):
        self.path = path
        self.hashes = hashes
        self.is_malicious = is_malicious

    def set_path(self, path: str):
        self.path = path

    def add_hash(self, hash_type: str, hash_value: str):
       self.hashes[hash_type] = hash_value
        
    def set_is_malicious(self, is_malicious: bool):
        self.is_malicious = is_malicious

    def __str__(self):
        return f"File(path={self.path}, md5hash={self.md5hash}, is_malicious={self.is_malicious})"
