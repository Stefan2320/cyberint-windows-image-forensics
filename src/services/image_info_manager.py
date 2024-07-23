# Local application imports
from src.utils.image_info import ImageInfo
from src.utils.system_details import SystemDetails
from src.services.repository_manager import RepositoryManager
from src.services.registry_extractor import (
    HostExtractor,
    UserExtractor,
    IPExtractor,
    GUIDExtractor
)
from src.services.registry_persistence import RegistryPersistence
from src.services.file_persistence import FilePersistence


class ImageInfoManager:
    def __init__(self, system_details: SystemDetails, repo_manager: RepositoryManager):
        self.system_details = system_details
        self.repo_manager = repo_manager
        self.image_details = None
        self.image_id = None
        self.host_extractor = HostExtractor("ComputerName")
        self.user_extractor = UserExtractor("ProfileList")
        self.ip_extractor = IPExtractor("Tcpip\\Parameters\\Interface")
        self.guid_extractor = GUIDExtractor("MachineGuid")

    def initialize_image(self) -> None:
        """
        Initializes the image and adds it to the repository.
        """
        self.system_details.initialize()
        windows_image = self.repo_manager.get_windows_image_repo().add_image("Test")
        self.image_id = windows_image.image_id

    def extract_and_store_image_info(self) -> None:
        """
        Extracts and stores image information in the database.
        """
        self.image_details = ImageInfo(
            user_extractor=self.user_extractor,
            host_extractor=self.host_extractor,
            ip_extractor=self.ip_extractor,
            guid_extractor=self.guid_extractor
        )
        self.image_details.set_location(self.system_details.C_drive)
        self._extract_and_store_guid()
        self._extract_and_store_ip()
        self._extract_and_store_hosts()
        self._extract_and_store_users()

    def _extract_and_store_guid(self) -> None:
        self.image_details.extract_GUID()
        self.repo_manager.get_image_guid_repo().add_guid(self.image_id, self.image_details.GUID)

    def _extract_and_store_ip(self) -> None:
        self.image_details.extract_ip()
        self.repo_manager.get_image_ip_repo().add_ip_set(self.image_id, self.image_details.ip)

    def _extract_and_store_hosts(self) -> None:
        self.image_details.extract_hosts()
        self.repo_manager.get_image_host_repo().add_host_set(self.image_id, self.image_details.hosts)

    def _extract_and_store_users(self) -> None:
        self.image_details.extract_users()
        self.repo_manager.get_image_user_repo().add_user_set(self.image_id, self.image_details.users)

    def check_persistence(self) -> None:
        """
        Checks registry and file persistence mechanisms and stores the findings in the database.
        """
        checker_registry = RegistryPersistence()
        file_checker = FilePersistence(self.system_details.C_drive)

        reg_run = checker_registry.extract_run_key(self.system_details.C_drive)
        self.repo_manager.get_image_persistence_repo().add_persistence_list(self.image_id, reg_run, "run")
        reg_run_once = checker_registry.extract_runOnce_key(self.system_details.C_drive)
        self.repo_manager.get_image_persistence_repo().add_persistence_list(self.image_id, reg_run_once, "runOnce")

        sys_persistence = file_checker.find_system_persistence()
        self.repo_manager.get_image_persistence_repo().add_persistence_list(self.image_id, sys_persistence, "system")

        if self.image_details and self.image_details.users:
            usr_persistence = file_checker.find_user_persistence(self.image_details.users)
            self.repo_manager.get_image_persistence_repo().add_persistence_list(self.image_id, usr_persistence, "user")
