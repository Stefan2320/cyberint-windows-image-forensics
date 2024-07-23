from src.services.hashers import MD5Hasher, SHA1Hasher
from src.services.files_parser import FilesParser
from src.services.vt_api import VTapi
from src.utils.file_helper import File
from src.utils.system_details import SystemDetails
from src.services.repository_manager import RepositoryManager
from src.config import get_api_key
from src.exceptions import exceptions

class FileProcessor:
    def __init__(self, system_details: SystemDetails, repo_manager: RepositoryManager):
        self.system_details = system_details
        self.repo_manager = repo_manager
        self.parser = None
        self.vt_api = None
        self.image_id = None

    def setup_parser(self) -> None:
        """
        Sets up the file parser with MD5 and SHA1 hashers.
        """
        md5hasher = MD5Hasher()
        sha1hasher = SHA1Hasher()
        self.parser = FilesParser(self.system_details.drives, md5hasher)
        self.parser.add_hasher(sha1hasher)

    def parse_files_and_hash(self) -> None:
        """
        Parses files and calculates their hashes.
        """
        self.parser.parse_drives_and_calculate_hash()

    def connect_to_vt(self) -> None:
        """
        Connects to the VirusTotal API.
        """
        api_key = get_api_key()
        if api_key is None:
            raise exceptions.APIKeyVTError()

        self.vt_api = VTapi(api_key)

    def process_files_and_store_in_db(self) -> None:
        """
        Processes files, checks their hashes with VirusTotal, and stores the information in the database.
        """
        for file_hash_path in self.parser.hashes:
            try:
                self._process_single_file(file_hash_path)
            except Exception as e:
                print(f"Error processing file {file_hash_path['name']}: {e}")
        self.vt_api.close_connection()
    
    def set_image_id(self, image_id: int) -> None:
        """
        Set the image id for the files which will be stored in the database. 
        """
        self.image_id = image_id
        
    def _process_single_file(self, file_hash_path: dict) -> None:
        """
        Processes a single file.
        """
        path = file_hash_path['path']
        hashes = file_hash_path['hashes']
        name = file_hash_path['name']
        
        file = File(path=path, name=name)
        self._add_hashes_to_file(file, hashes)
        self._check_with_virustotal(file)
        self._store_file_in_db(file)

    def _add_hashes_to_file(self, file: File, hashes: dict) -> None:
        """
        Adds hashes to the file.
        """
        for hash_type, hash_value in hashes.items():
            file.add_hash(hash_type, hash_value)

    def _check_with_virustotal(self, file: File) -> None:
        """
        Checks the file's hashes with VirusTotal.
        """
        for hash_type, hash_value in file.hashes.items():
            vt_response = self.vt_api.get_file(hash_value)
            if vt_response:
                file.is_malicious = (vt_response.last_analysis_stats['malicious'] + vt_response.last_analysis_stats['suspicious'] > vt_response.last_analysis_stats['harmless'])

    def _store_file_in_db(self, file: File) -> None:
        """
        Stores the file and its hashes in the database.
        """
        file_repo = self.repo_manager.get_image_file_repo().add_file(self.image_id, file.path, file.is_malicious)
        for hash_type in ['MD5', 'SHA1']:
            self.repo_manager.get_file_hash_repo().add_hash(file_repo.file_id, hash_type, file.hashes.get(hash_type))
