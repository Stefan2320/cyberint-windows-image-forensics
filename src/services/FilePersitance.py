
import os


class FilePersistance:

    system_persistance_path = "ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"

    def __init__(self, root_directory) -> None:
        self.root_directory = root_directory.replace('/','\\') + '\\'
        self.user_persistance = []
        self.system_persistance = []
        pass
   
    def find_user_persistance(self, usernames: list[str]):
        for user in usernames:
            file_path = self.root_directory + f"Users\{user}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"   
            files = os.listdir(file_path) 
            self.user_persistance.append(files)

    def find_system_persistance(self):
        file_path = self.root_directory + self.system_persistance_path
        files = os.listdir(file_path) 
        self.system_persistance = files
    