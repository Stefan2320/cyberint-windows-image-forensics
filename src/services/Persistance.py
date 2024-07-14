from src.repository.FileRepo import FileRepository

class FileService:
    def __init__(self, repository: FileRepository):
        self.repository = repository

    def check_any_file_is_malicious(self):
        '''add return type'''
        return self.repository.get_unknown_files()
 
    def check_persistance_for_file(self):
        '''
        '''
        files = self.check_any_file_is_malicious()
        for file in files:
            print(file.name, file.path) 
