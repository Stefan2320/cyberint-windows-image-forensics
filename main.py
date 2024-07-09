from src.models.ImageInfo import ImageInfo
from src.models.SystemDetails import SystemDetails
from src.services.Hashing import MD5Hasher
from src.services.Parser import FilesParser
from src.models.Info_extractor import (HostExtractor,
                                       UserExtractor,
                                       IPExtractor,
                                       GUIDExtractor)

system_details = SystemDetails()
system_details.initialize()

host_extractor = HostExtractor("ComputerName")
user_extractor = UserExtractor("ProfileList")
ip_extractor = IPExtractor("TCPIP")
guid_extractor = GUIDExtractor("MachineGuid")

image_details = ImageInfo(user_extractor, host_extractor, ip_extractor, guid_extractor)
image_details.set_location(system_details.C_drive)

# image_details.extract_GUID()
# image_details.extract_ip()
# image_details.extract_hosts()
# image_details.extract_users()

# print(image_details.GUID)
# print(image_details.ip)
# print(image_details.hosts)
# print(image_details.users)

md5hasher = MD5Hasher()
parser = FilesParser(system_details.drives, md5hasher)
parser.parse_drives()


