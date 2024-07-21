from Registry import Registry
from .Info_extractor import (UserExtractor,
                            HostExtractor,
                            IPExtractor,
                            GUIDExtractor
                                       )
                                       
class ImageInfo:
    # add how to saved data looks like
    def __init__(self, user_extractor: UserExtractor = None, host_extractor: HostExtractor = None, ip_extractor: IPExtractor = None, guid_extractor: GUIDExtractor = None):
        self.user_extractor = user_extractor
        self.host_extractor = host_extractor
        self.ip_extractor = ip_extractor
        self.guid_extractor = guid_extractor
        self.users =  set()
        self.hosts = set() 
        self.ip : dict[str, list] = {} 
        self.GUID = None

    def set_location(self, location: str):
        self.location = location

    def extract_users(self):
        '''
        TODO filter if S-1-5-18 etc are relevant or not + check info
        also verify errors
        '''
        _users = self.user_extractor.extract(self.location)
        for registry in _users:
            if 'ProfileImagePath' in registry.keys():
                SID = registry['ProfileImagePath'][1]
                SID = SID[SID.find('\\CurrentVersion'):-1]
                self.user_extractor.set_reg_key(SID)
                for reg_users in self.user_extractor.extract(self.location):
                    if any('Users' in path for path in reg_users['ProfileImagePath']):
                        username = reg_users['ProfileImagePath'][0][reg_users['ProfileImagePath'][0].rfind('\\'):].replace('\\','')
                        self.users.add(username)
            
    def extract_hosts(self):
        hosts = self.host_extractor.extract(self.location)
        for host_keys in hosts:
            if host_keys.get('ComputerName'):
                self.hosts.add(host_keys['ComputerName'][0])

    def extract_ip(self):
        important_keys = ['DhcpServer','DhcpIPAddress','DhcpNameServer','IPAddress']
        ip = self.ip_extractor.extract(self.location)
        for ip_keys in ip:
            if ip_keys.get('Domain'):
                properties = [] 
                domain = ip_keys.get('Domain')[1]
                domain = domain[domain.rfind('{'):-1]
                self.ip_extractor.set_reg_key(domain)
                for ip_sub_keys in self.ip_extractor.extract(self.location):
                    for key in ip_sub_keys.keys():
                        if key in important_keys:
                            properties.append({key,ip_sub_keys[key][0]})
                self.ip[domain[domain.rfind('{'):]] = properties

    def extract_GUID(self):
        GUID = self.guid_extractor.extract(self.location)
        if GUID.get('MachineGuid'):
            self.GUID = GUID['MachineGuid'][0]  