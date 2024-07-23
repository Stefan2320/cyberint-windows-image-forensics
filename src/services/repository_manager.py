from src.repository.windows_image_table import WindowsImageTable
from src.repository.image_file_table import ImageFileTable
from src.repository.file_hash_table import FileHashTable
from src.repository.image_host_table import ImageHostTable
from src.repository.image_ip_table import ImageIPTable
from src.repository.image_user_table import ImageUserTable
from src.repository.image_guid_table import ImageGUIDTable
from src.repository.file_persistence_table import FilePersistenceTable 

from src.repository.init  import SessionLocal, create_database

class RepositoryManager:
    def __init__(self) -> None:
        self.session = None
        self.windows_image_repo = None
        self.image_file_repo = None
        self.file_hash_repo = None
        self.image_host_repo = None
        self.image_ip_repo = None
        self.image_user_repo = None
        self.image_guid_repo = None
        self.image_persistence_repo = None

    def initialize(self) -> None:
        """
        Initializes the database and repository objects.
        """
        create_database()
        self.session = SessionLocal()
        self.windows_image_repo = WindowsImageTable(self.session)
        self.image_file_repo = ImageFileTable(self.session)
        self.file_hash_repo = FileHashTable(self.session)
        self.image_host_repo = ImageHostTable(self.session)
        self.image_ip_repo = ImageIPTable(self.session)
        self.image_user_repo = ImageUserTable(self.session)
        self.image_guid_repo = ImageGUIDTable(self.session)
        self.image_persistence_repo = FilePersistenceTable(self.session)

    def close(self) -> None:
        """
        Closes the database session.
        """
        if self.session:
            self.session.close()

    def get_windows_image_repo(self) -> WindowsImageTable:
        """
        Returns the WindowsImageTable repository.
        """
        return self.windows_image_repo

    def get_image_file_repo(self) -> ImageFileTable:
        """
        Returns the ImageFileTable repository.
        """
        return self.image_file_repo

    def get_file_hash_repo(self) -> FileHashTable:
        """
        Returns the FileHashTable repository.
        """
        return self.file_hash_repo

    def get_image_host_repo(self) -> ImageHostTable:
        """
        Returns the ImageHostTable repository.
        """
        return self.image_host_repo

    def get_image_ip_repo(self) -> ImageIPTable:
        """
        Returns the ImageIPTable repository.
        """
        return self.image_ip_repo

    def get_image_user_repo(self) -> ImageUserTable:
        """
        Returns the ImageUserTable repository.
        """
        return self.image_user_repo

    def get_image_guid_repo(self) -> ImageGUIDTable:
        """
        Returns the ImageGUIDTable repository.
        """
        return self.image_guid_repo

    def get_image_persistence_repo(self) -> FilePersistenceTable:
        """
        Returns the FilePersistenceTable repository.
        """
        return self.image_persistence_repo
