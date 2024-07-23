import os
from src.utils.abstract_hasher import Hasher


class FilesParser:
    def __init__(self, drives: list[str], hasher: Hasher) -> None:
        """
        Initializes the FilesParser with drives to scan and a hasher instance.

        Args:
            drives (list[str]): A list of drive paths to parse.
            hasher (Hasher): An instance of a Hasher for computing file hashes.
        """
        self.drives = drives
        self.hasher: list[Hasher] = [hasher]
        self.hashes: list[dict[str, str]] = []

    def calculate_hash_helper(self, file: str) -> dict[str, str]:
        """
        Computes hashes for a given file using the provided hasher instances.

        Returns:
            dict[str, str]: A dictionary where the keys are hash types and the values are the computed hashes.
        """
        all_hashes_file = {}
        for hash_type in self.hasher:
            hash_value = hash_type.compute_hash(file)
            all_hashes_file[hash_type.get_hash_type()] = hash_value
        return all_hashes_file

    def recursive_parser(self, dir: str) -> None:
        """
        Recursively parses directories, computes hashes for files, and stores results.
        """
        all_files = os.listdir(dir)
        files = [f for f in all_files if os.path.isfile(os.path.join(dir, f))]
        dirs = [d for d in all_files if os.path.isdir(os.path.join(dir, d))]
        
        for file in files:
            file_path = os.path.join(dir, file)
            all_hashes = self.calculate_hash_helper(file_path)
            self.hashes.append({'path': file_path, 'name': file, 'hashes': all_hashes})
        
        for d in dirs:
            self.recursive_parser(os.path.join(dir, d))

    def parse_drives_and_calculate_hash(self) -> None:
        """
        Parses all specified drives and calculates hashes for files on those drives.
        """
        for drive in self.drives:
            self.recursive_parser(drive)

    def add_hasher(self, new_hasher: Hasher) -> None:
        """
        Adds a new hasher instance to the list of hashers.

        Args:
            new_hasher (Hasher): An instance of a Hasher to add.
        """
        self.hasher.append(new_hasher)
