import os
from src.models.Hash import Hasher

"""
TODO threading for recursion    
"""

class FilesParser:
    def __init__(self, drives: list[str], hasher: Hasher) -> None:
        self.drives = drives
        self.hasher : list[Hasher] = [hasher]
        # hashes will store at one position the path of the file and a dictionary with all the hashes
        self.hashes : list[dict[str:str]]= [] 
        
    def calculate_hash_helper(self, file: str): 
        all_hashes_file = {}
        for hash_type in self.hasher:
                hash = hash_type.compute_hash(file)
                all_hashes_file[hash_type.get_hash_type()] = hash
        return all_hashes_file 

    def recursive_parser(self, dir: str): 
        '''
        When saving to a db maybe use a DBhandler that will be given in the constructor
        '''
        all_files = os.listdir(dir)
        files = [f for f in all_files if os.path.isfile(os.path.join(dir,f))]
        dirs = [d for d in all_files if os.path.isdir(os.path.join(dir,d))]
        for file in files:
            file_path = os.path.join(dir,file)
            all_hashes = self.calculate_hash_helper(file_path)
            self.hashes.append({'path':file_path,'name':file,'hashes':all_hashes})
        for d in dirs:
            self.recursive_parser(os.path.join(dir,d))

    def parse_drives_and_calculate_hash(self):
        for drive in self.drives:
            self.recursive_parser(drive)
                    
    def add_hasher(self, new_hasher: Hasher):
        self.hasher.append(new_hasher) 
         