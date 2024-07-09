import os
from src.models.Hash import Hasher


class FilesParser:
    def __init__(self, drives: list[str], hasher: Hasher) -> None:
        self.drives = drives
        self.hasher = hasher
    
    def recursive_parser(self, dir: str): 
        '''
        When saving to a db maybe use a DBhandler that will be given in the constructor
        '''
        all_files = os.listdir(dir)
        files = [f for f in all_files if os.path.isfile(os.path.join(dir,f))]
        dirs = [d for d in all_files if os.path.isdir(os.path.join(dir,d))]
        for file in files:
            hash = self.hasher.compute_hash(os.path.join(dir,file))
        for d in dirs:
            self.recursive_parser(os.path.join(dir,d))
    
    def parse_drives(self):
        for drive in self.drives:
            self.recursive_parser(drive)
                    
            
         