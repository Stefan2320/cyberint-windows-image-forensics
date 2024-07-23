from src.services.registry_extractor import (
    UserExtractor,
    HostExtractor,
    IPExtractor,
    GUIDExtractor
)


class ImageInfo:
    """
    Extracts and stores various information related to an image, including users, hosts, IP addresses, and GUIDs.

    Attributes:
        user_extractor (UserExtractor): Extractor for user-related data.
        host_extractor (HostExtractor): Extractor for host-related data.
        ip_extractor (IPExtractor): Extractor for IP-related data.
        guid_extractor (GUIDExtractor): Extractor for GUID-related data.
        users (set): Set of extracted usernames.
        hosts (set): Set of extracted hostnames.
        ip (dict): Dictionary mapping domains to IP-related properties (from the registries).
        GUID (str or None): Extracted machine GUID.
        location (str): File path or location for extraction.
    """

    def __init__(self, user_extractor: UserExtractor = None, 
                 host_extractor: HostExtractor = None,
                 ip_extractor: IPExtractor = None,
                 guid_extractor: GUIDExtractor = None):
        """
        Initializes an ImageInfo instance.

        Args:
            user_extractor (UserExtractor, optional): Instance of UserExtractor. Defaults to None.
            host_extractor (HostExtractor, optional): Instance of HostExtractor. Defaults to None.
            ip_extractor (IPExtractor, optional): Instance of IPExtractor. Defaults to None.
            guid_extractor (GUIDExtractor, optional): Instance of GUIDExtractor. Defaults to None.
        """
        self.user_extractor = user_extractor
        self.host_extractor = host_extractor
        self.ip_extractor = ip_extractor
        self.guid_extractor = guid_extractor
        self.users = set()
        self.hosts = set()
        self.ip = {}  # Type: dict[str, list]
        self.GUID = None
        self.location = None

    def set_location(self, location: str) -> None:
        """
        Sets the location of the root folder (the equivalent of the C: directory). This needs to be set so we can read from the 
        registries which are located there.

        Args:
            location (str): The file path or location to be set (equivalent of C directory).
        """
        self.location = location

    def extract_users(self) -> None:
        """
        Extract all users from the Windows image. 
        """
        if self.user_extractor and self.location:
            _users = self.user_extractor.extract(self.location)
            for registry in _users:
                if 'ProfileImagePath' in registry:
                    sid = registry['ProfileImagePath'][1]
                    sid = sid[sid.find('\\CurrentVersion'):-1]
                    self.user_extractor.set_reg_key(sid)
                    for reg_users in self.user_extractor.extract(self.location):
                        if any('Users' in path for path in reg_users.get('ProfileImagePath', [])):
                            username = reg_users['ProfileImagePath'][0]
                            username = username[username.rfind('\\'):]
                            self.users.add(username.replace('\\', ''))

    def extract_hosts(self) -> None:
        """
        Extract all hosts from the Windows image.
        """
        if self.host_extractor and self.location:
            hosts = self.host_extractor.extract(self.location)
            for host_keys in hosts:
                if 'ComputerName' in host_keys:
                    self.hosts.add(host_keys['ComputerName'][0])
                hosts = self.host_extractor.extract(self.location)

    def extract_ip(self) -> None:
        """
        Extracts IP-related information from the Windows image. The values considered important from the registry keys are in the
        important_keys list and only those will be extracted if found.  
        """
        if self.ip_extractor and self.location:
            important_keys = ['DhcpServer', 'DhcpIPAddress', 'DhcpNameServer', 'IPAddress']
            ip = self.ip_extractor.extract(self.location)
            for ip_keys in ip:
                if 'Domain' in ip_keys:
                    domain = ip_keys['Domain'][1]
                    domain = domain[domain.rfind('{'):-1]
                    self.ip_extractor.set_reg_key(domain)
                    properties = []
                    for ip_sub_keys in self.ip_extractor.extract(self.location):
                        for key in ip_sub_keys:
                            if key in important_keys:
                                properties.append({key: ip_sub_keys[key][0]})
                self.ip[domain[domain.rfind('{'):]] = properties

    def extract_GUID(self) -> None:
        """
        Extracts the machine GUID from the Windows image.
        """
        if self.guid_extractor and self.location:
            guid = self.guid_extractor.extract(self.location)
            if 'MachineGuid' in guid:
                self.GUID = guid['MachineGuid'][0]
