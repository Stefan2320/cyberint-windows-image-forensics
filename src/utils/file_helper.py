class File:
    """
    Represents a file with associated metadata such as hashes, path, name, and malicious status.
    This class is used as a helper; the data will be stored in two tables in the database:
        - File table
        - Hash table

    Attributes:
        name (str): The name of the file.
        path (str): The file path.
        hashes (dict): A dictionary where the key is the hash type and the value is the hash value.
        is_malicious (bool): Indicates whether the file is malicious.
    """

    def __init__(self, hashes=None, path=None, is_malicious=None, name=None):
        """
        Initializes a File instance.

        Args:
            hashes (dict, optional): A dictionary of hash types and their values. Defaults to an empty dictionary if not provided.
            path (str, optional): The file path. Defaults to None.
            is_malicious (bool, optional): Indicates if the file is malicious. Defaults to None.
            name (str, optional): The name of the file. Defaults to None.
        """
        self.name = name
        self.path = path
        self.hashes = hashes if hashes is not None else {}
        self.is_malicious = is_malicious

    def set_name(self, name: str) -> None:
        """
        Sets the name of the file.
        """
        self.name = name

    def set_path(self, path: str) -> None:
        """
        Sets the file path.
        """
        self.path = path

    def add_hash(self, hash_type: str, hash_value: str) -> None:
        """
        Adds a hash to the file's hash dictionary.
        """
        self.hashes[hash_type] = hash_value

    def set_is_malicious(self, is_malicious: bool) -> None:
        """
        Sets the malicious status of the file.
        """
        self.is_malicious = is_malicious

    def __str__(self) -> str:
        """
        Returns a string representation of the File instance.
        """
        return (f"File(name={self.name}, path={self.path}, "
                f"hashes={self.hashes}, is_malicious={self.is_malicious})")

