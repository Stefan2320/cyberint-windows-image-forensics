
import os


class FilePersistance:

#    user_persistance = "Users\USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    system_persistance = "ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"

    def __init__(self, root_directory) -> None:
        self.root_directory = root_directory.replace('/','\\') + '\\'
        pass
   
    def find_system_persistance(self):
        pass

    def find_system_persistance(self):
        file_path = self.root_directory + self.system_persistance
        files = os.listdir(file_path) 
    