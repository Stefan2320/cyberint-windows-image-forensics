
from src.services.repository_manager import RepositoryManager
from src.services.system_manger import SystemManager
from src.utils.FTImager_script import mount,unmount_images

user_input = mount()
database_manager = RepositoryManager()
database_manager.initialize()
print("[+] Database initialized")
manager = SystemManager(database_manager)
manager.initialize_system()
print("[+] Manage initialized")
manager.extract_image_info()
print("[+] Extracted information about image")
manager.setup_parser()
print("[+] Created file parser")
manager.parse_files_and_hash()
print("[+] Parsed and computed hash")
manager.connect_to_vt()
print("[+] Conntected to vt api")
manager.process_files_and_store_in_db()
print("[+] Stored file and hash in database")
manager.check_persistence()
print("[+] Files that have persistence were added")
if user_input.lower() == "y":
    unmount_images()