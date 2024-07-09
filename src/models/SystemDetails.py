import os
from ..exceptions.exceptions import DriveError

class SystemDetails():
    
    def __init__(self): 
        self.drives = []
        self.C_drive = None
        

    def find_new_drives(self):
        '''
        Searching for the mounted drives, by default it's considered that there are only two default drivers mounted (C and D).
        The new drives are stored in an array.
        '''
        drives = []
        for drive_letter in 'ABEFGHIJKLMNOPQRSTUVWXYZ':
            if os.path.exists(f'{drive_letter}:'):
                drives.append(drive_letter+":/")
            else:
                pass
        self.drives = drives


    def find_C_drive(self):
        '''
        Search the C: equivalent that was mounted on the PC. We will look for the folders: 'Users','Windows' and 'Program Files'
        (If another partition has these directories then it will fail)
        '''
        C_drive = ['Users','Windows','Program Files']
        drives = self.drives + [ drive+"[root]" for drive in self.drives]
        for drive in drives:
            if os.path.exists(drive):
                directories =  os.listdir(drive)
                if C_drive[0] in directories and C_drive[1] in directories and C_drive[2] in directories:
                    self.C_drive = drive
        
        if self.C_drive is None:
            raise DriveError("An error occured while trying to find the 'C:\\' drive from the mounted image. Please take note that if there are multiple partitions or no \
                              partition with the following directories: 'Users', 'Windows' and 'Program Files' it will fail.")

    def initialize(self):
        self.find_new_drives()
        self.find_C_drive()
        

    