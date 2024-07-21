from sqlalchemy.orm import Session
from src.repository.WindowsImage import WindowsImageRepository
from src.repository.ImageFileRepository import ImageFileRepository
from src.repository.FileHashRepository import FileHashRepository
from src.repository.ImageHostRepository import ImageHostRepository
from src.repository.ImageIPRepository import ImageIPRepository
from src.repository.ImageUserRepository import ImageUserRepository
from src.repository.ImageGUIDRepository import ImageGUIDRepository
from src.repository.PersistanceRepository import ImagePersistanceRepository

from src.repository.init  import SessionLocal, create_database

class RepositoryManager:
    def __init__(self):
        self.session = None
        self.windows_image_repo = None
        self.image_file_repo = None
        self.file_hash_repo = None
        self.image_host_repo = None

    def initialize(self):
        create_database()
        self.session = SessionLocal()
        self.windows_image_repo = WindowsImageRepository(self.session)
        self.image_file_repo = ImageFileRepository(self.session)
        self.file_hash_repo = FileHashRepository(self.session)
        self.image_host_repo = ImageHostRepository(self.session)
        self.image_ip_repo = ImageIPRepository(self.session)
        self.image_user_repo = ImageUserRepository(self.session)
        self.image_guid_repo = ImageGUIDRepository(self.session)
        self.image_persistence_repo = ImagePersistanceRepository(self.session)

    def close(self):
        if self.session:
            self.session.close()

    def get_windows_image_repo(self):
        return self.windows_image_repo

    def get_image_file_repo(self):
        return self.image_file_repo

    def get_file_hash_repo(self):
        return self.file_hash_repo

    def get_image_host_repo(self):
        return self.image_host_repo

    def get_image_ip_repo(self):
        return self.image_ip_repo

    def get_image_user_repo(self):
        return self.image_user_repo

    def get_image_guid_repo(self):
        return self.image_guid_repo

    def get_image_persistance_repo(self):
        return self.image_persistence_repo
    