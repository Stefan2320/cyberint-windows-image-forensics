from abc import ABC, abstractmethod
from Registry import Registry

class Extractor(ABC):

    def __init__(self, keyword: str = None):
        self.keyword = keyword
        
    @abstractmethod
    def extract(self, location: str):
        pass

    def rec(self, key, keyword: str,paths=None,depth=0):
        if paths is None:
            paths = []
        if keyword in key.path():
            paths.append(key.path())
        for subkey in key.subkeys():
            self.rec(subkey,keyword, paths,depth + 1)
        return paths

class UserExtractor(Extractor):
    def extract(self, location: str):
        self.users = []
        reg = Registry.Registry(f"{location}/Windows/System32/config/SOFTWARE")
        keys = self.rec(reg.root(),self.keyword)
        # TODO
        # regex_pattern = r"S-[a-zA-Z0-9\-]+"
        # p = re.compile(regex_pattern)
        # for element in list(keys):
        #     print(p.match(element))
        #     if p.match(element):
        #         print(element)
        for subkeys in keys: 
            key = reg.open(subkeys[5:])
            for value in [v for v in key.values() \
                            if v.value_type() == Registry.RegSZ or \
                                v.value_type() == Registry.RegExpandSZ]:
                self.users.append({value.name():[value.value(), str(key)[:-28]]})
        return self.users

class HostExtractor(Extractor):
    '''
    '''
    def extract(self, location: str):
        '''
        TODO who is location??
        '''
        self.hosts = []
        reg = Registry.Registry(f"{location}/Windows/System32/config/SYSTEM")
        keys = self.rec(reg.root(),self.keyword)
        for subkeys in keys: 
            key = reg.open(subkeys[5:])
            for value in [v for v in key.values() \
                            if v.value_type() == Registry.RegSZ or \
                                v.value_type() == Registry.RegExpandSZ]:
                self.hosts.append({value.name():[value.value(), str(key)[:-28]]})
        return self.hosts

class IPExtractor(Extractor):
    def extract(self, location: str):
        '''
        '''
        self.ip = []
        reg = Registry.Registry(f"{location}/Windows/System32/config/SYSTEM")
        keys = self.rec(reg.root(),self.keyword)
        for subkeys in keys: 
            key = reg.open(subkeys[5:])
            for value in [v for v in key.values() \
                            if v.value_type() == Registry.RegSZ or \
                                v.value_type() == Registry.RegExpandSZ]:
                self.ip.append({value.name():[value.value(), str(key)[:-28]]})
        return self.ip

class GUIDExtractor(Extractor):
    def extract(self, location: str):
        '''
        '''
        reg = Registry.Registry(f"{location}/Windows/System32/config/SOFTWARE")
        key = reg.open("Microsoft\\Cryptography")
        for value in [v for v in key.values() if v.value_type() in [Registry.RegSZ, Registry.RegExpandSZ]]:
            if value.name() == self.keyword:
                return {value.name(): [value.value(),str(key)[:-28]]}
                break
        return None 
