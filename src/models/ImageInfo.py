from Registry import Registry
from .Info_extractor import (UserExtractor,
                                       HostExtractor,
                                       IPExtractor,
                                       GUIDExtractor
                                       )
                                       
#TODO read the values from the registry keys
class ImageInfo:
    def __init__(self, user_extractor: UserExtractor, host_extractor: HostExtractor, ip_extractor: IPExtractor, guid_extractor: GUIDExtractor):
        self.user_extractor = user_extractor
        self.host_extractor = host_extractor
        self.ip_extractor = ip_extractor
        self.guid_extractor = guid_extractor
        self.users = []
        self.hosts = []
        self.ip = []
        self.GUID = None

    def set_location(self, location: str):
        self.location = location

    def extract_users(self):
        self.users = self.user_extractor.extract(self.location)

    def extract_hosts(self):
        self.hosts = self.host_extractor.extract(self.location)

    def extract_ip(self):
        self.ip = self.ip_extractor.extract(self.location)

    def extract_GUID(self):
        self.GUID = self.guid_extractor.extract(self.location)
 