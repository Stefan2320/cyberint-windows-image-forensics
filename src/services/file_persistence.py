import os

class FilePersistence:

    system_persistence_path = "ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp"

    def __init__(self, root_directory: str) -> None:
        """
        Initializes the FilePersistence class with the equivalent root directory for the image.
        """
        self.root_directory = root_directory.replace('/', '\\') + '\\'
        self.user_persistence = []
        self.system_persistence = []

    def find_user_persistence(self, usernames: list[str]) -> list[str]:
        """
        Finds user persistence files in the startup directories of the specified users.
        
        Args:
            usernames (list[str]): A list of Windows users to search for the files.
        
        Returns:
            list[str]: A list of user persistence file names.
        """
        for user in usernames:
            file_path = os.path.join(self.root_directory, f"Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
            try:
                files = os.listdir(file_path)
                self.user_persistence.extend(files)
            except FileNotFoundError:
                continue
        return self.user_persistence

    def find_system_persistence(self) -> list[str]:
        """
        Finds system persistence files in the startup directory.
        
        Returns:
            list[str]: A list of system persistence file names.
        """
        file_path = os.path.join(self.root_directory, self.system_persistence_path)
        try:
            files = os.listdir(file_path)
            self.system_persistence = files
        except FileNotFoundError:
            self.system_persistence = []
        return self.system_persistence
