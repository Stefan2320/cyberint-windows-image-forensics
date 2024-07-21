from src.models.ImageInfo import ImageInfo
from src.models.SystemDetails import SystemDetails
from src.repository.init import SessionLocal
from src.repository.models import FileModel
from src.services.Hashing import (MD5Hasher,
                                 SHA1Hasher)
from src.services.Parser import FilesParser
from src.models.Info_extractor import (HostExtractor,
                                       UserExtractor,
                                       IPExtractor,
                                       GUIDExtractor,
                                       Extractor,
                                       GeneralExtractor)
from src.config import get_api_key
from src.services.vt_api import VTapi
from src.exceptions import exceptions 
from src.models.Files import File
from src.repository.init import create_database
from src.services.RegistryPersistance import PersistenceCheckerRegistry
from src.services.FilePersitance import FilePersistance
from src.services.ReposirotyManager import RepositoryManager

class SystemManager:
    def __init__(self, repo_manager: RepositoryManager):
        self.system_details = SystemDetails()
        self.host_extractor = HostExtractor("ComputerName")
        self.user_extractor = UserExtractor("ProfileList")
        self.ip_extractor = IPExtractor("Tcpip\\Parameters\\Interface")
        self.guid_extractor = GUIDExtractor("MachineGuid")
        self.image_details = None
        self.parser = None
        self.session = None
        self.vt_api = None
        self.repo_manager = repo_manager
                
    def initialize_system(self):
        self.system_details.initialize()
        windows_image = self.repo_manager.get_windows_image_repo().add_image("Test")
        self.image_id = windows_image.image_id

    def extract_image_info(self):
        self.image_details = ImageInfo(
            user_extractor=self.user_extractor,
            host_extractor=self.host_extractor,
            ip_extractor=self.ip_extractor,
            guid_extractor=self.guid_extractor
        )
        self.image_details.set_location(self.system_details.C_drive)
        self.image_details.extract_GUID()
        self.image_details.extract_ip()
        self.image_details.extract_hosts()
        self.image_details.extract_users()
        self.repo_manager.get_image_guid_repo().add_guid(self.image_id,self.image_details.GUID)
        self.repo_manager.get_image_ip_repo().add_ip_set(self.image_id,self.image_details.ip)
        self.repo_manager.get_image_user_repo().add_user_set(self.image_id,self.image_details.users)
        self.repo_manager.get_image_host_repo().add_host_set(self.image_id, self.image_details.hosts)
        
    def setup_parser(self):
        md5hasher = MD5Hasher()
        sha1hasher = SHA1Hasher()
        self.parser = FilesParser(self.system_details.drives, md5hasher)
        self.parser.add_hasher(sha1hasher)

        self.parser = FilesParser(["E://"], md5hasher)
        self.parser.add_hasher(sha1hasher)

    def parse_files_and_hash(self):
        self.parser.parse_drives_and_calculate_hash()
        
    def connect_to_vt(self):
        api_key = get_api_key()
        if api_key is None:
            raise exceptions.APIKeyVTError()

        self.vt_api = VTapi(api_key)

    def process_files_and_store_in_db(self):
        for file_hash_path in self.parser.hashes:
            path = file_hash_path['path']
            hash = file_hash_path['hashes']
            name = file_hash_path['name']
            try:
                file = File(path=path, name=name)
                for hash_type, hash_value in hash.items():
                    file.add_hash(hash_type, hash_value)
                    f = self.vt_api.get_file(hash_value)
                    if f:
                        file.is_malicious = (f.last_analysis_stats['malicious'] + f.last_analysis_stats['suspicious'] > f.last_analysis_stats['harmless'])
                file_repo = self.repo_manager.get_image_file_repo().add_file(self.image_id,file.path,file.is_malicious)
                self.repo_manager.get_file_hash_repo().add_hash(file_repo.file_id,'MD5',file.hashes.get('MD5'))
                self.repo_manager.get_file_hash_repo().add_hash(file_repo.file_id,'SHA1',file.hashes.get('SHA1'))
            except Exception as e:
                print(f"Error processing file {name}: {e}")
        self.vt_api.close_connection()

    def check_persistence(self):
        checker_registry = PersistenceCheckerRegistry()
        file_checker = FilePersistance(self.system_details.C_drive)

        reg_run = checker_registry.extract_run_key(self.system_details.C_drive)
        self.repo_manager.get_image_persistance_repo().add_persistence_list(self.image_id,reg_run,"run")
        reg_run_once = checker_registry.extract_runOnce_key(self.system_details.C_drive)
        self.repo_manager.get_image_persistance_repo().add_persistence_list(self.image_id,reg_run_once,"runOnce")

        sys_persistance = file_checker.find_system_persistance()
        self.repo_manager.get_image_persistance_repo().add_persistence_list(self.image_id,sys_persistance,"system")
        if self.image_details and self.image_details.users:
                usr_persistence = file_checker.find_user_persistance(self.image_details.users)
                self.repo_manager.get_image_persistance_repo().add_persistence_list(self.image_id,usr_persistence,"user")
