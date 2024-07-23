from src.services.image_info_manager import ImageInfoManager
from src.services.file_processor import FileProcessor
from src.utils.system_details import SystemDetails
from src.services.repository_manager import RepositoryManager

class SystemManager:
    def __init__(self, repo_manager: RepositoryManager):
        self.system_details = SystemDetails()
        self.image_info_manager = ImageInfoManager(self.system_details, repo_manager)
        self.file_processor = FileProcessor(self.system_details, repo_manager)


    def initialize_system(self) -> None:
        """
        Initializes the system and image.
        """
        self.image_info_manager.initialize_image()
        self.file_processor.set_image_id(self.image_info_manager.image_id)

    def extract_image_info(self) -> None:
        """
        Extracts and stores image information.
        """
        self.image_info_manager.extract_and_store_image_info()

    def setup_parser(self) -> None:
        """
        Sets up the file parser.
        """
        self.file_processor.setup_parser()

    def parse_files_and_hash(self) -> None:
        """
        Parses files and calculates their hashes.
        """
        self.file_processor.parse_files_and_hash()

    def connect_to_vt(self) -> None:
        """
        Connects to the VirusTotal API.
        """
        self.file_processor.connect_to_vt()

    def process_files_and_store_in_db(self) -> None:
        """
        Processes files, checks their hashes with VirusTotal, and stores the information in the database.
        """
        self.file_processor.process_files_and_store_in_db()

    def check_persistence(self) -> None:
        """
        Checks persistence mechanisms and stores the findings in the database.
        """
        self.image_info_manager.check_persistence()
