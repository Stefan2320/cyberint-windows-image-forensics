import os
from src.exceptions.exceptions import DriveError

class SystemDetails:
    """
    Class to manage and identify system drives, specifically focusing on finding the C: drive 
    from a mounted image.

    Attributes:
        drives (list): List of detected drives from the mounted image.
        C_drive (str): Path of the detected C: drive, if found.
    """

    def __init__(self):
        self.drives = []
        self.C_drive = None

    def find_new_drives(self) -> None:
        """
        Searches for mounted drives, excluding default drives (C: and D:). 
        The newly detected drives are stored in the `drives` attribute.
        """
        drives = []
        for drive_letter in 'ABEFGHIJKLMNOPQRSTUVWXYZ':
            if os.path.exists(f'{drive_letter}:'):
                drives.append(f'{drive_letter}:\\')
        self.drives = drives

    def find_C_drive(self) -> None:
        """
        Searches for the C: drive by checking for specific directories ('Users', 'Windows', 
        'Program Files') on the mounted drives. Sets the `C_drive` attribute if found.
        """
        required_directories = ['Users', 'Windows', 'Program Files']
        drives_to_check = self.drives + [drive + "[root]" for drive in self.drives]
        for drive in drives_to_check:
            if os.path.exists(drive):
                directories = os.listdir(drive)
                if all(dir_name in directories for dir_name in required_directories):
                    self.C_drive = drive
                    return
        
        raise DriveError(
            "An error occurred while trying to find the 'C:\\' drive from the mounted image. "
            "Please note that if there are multiple partitions or no partition with the directories: "
            "'Users', 'Windows', and 'Program Files', it will fail."
        )

    def initialize(self) -> None:
        self.find_new_drives()
        self.find_C_drive()
