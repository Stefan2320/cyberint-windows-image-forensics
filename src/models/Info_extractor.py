from abc import ABC, abstractmethod
from Registry import Registry

class Extractor(ABC):

    def __init__(self, reg_key: str = None):
        self.reg_key = reg_key
        
    @abstractmethod
    def extract(self, location: str = None):
        pass

    def rec(self, key, reg_key: str,paths=None,depth=0):
        if paths is None:
            paths = []
        if reg_key in key.path():
            paths.append(key.path())
        for subkey in key.subkeys():
            self.rec(subkey,reg_key, paths,depth + 1)
        return paths

class GeneralExtractor(Extractor):
    def __init__(self, location: str = None, reg_hive: str = None, reg_key: str = None):
        super().__init__()
        self.location = location
        self.reg_hive = reg_hive
        self.reg_key = reg_key
        
    def extract(self):
        self.data = []
        reg = Registry.Registry(self.location+self.reg_hive)
        keys = self.rec(reg.root(),self.reg_key)
        for subkeys in keys: 
            key = reg.open(subkeys[5:])
            for value in [v for v in key.values() \
                            if v.value_type() == Registry.RegSZ or \
                                v.value_type() == Registry.RegExpandSZ]:
                self.data.append({value.name():[value.value(), str(key)[:-28]]})
        return self.data

class UserExtractor(Extractor):
    def extract(self, location: str):
        self.users = []
        reg = Registry.Registry(f"{location}/Windows/System32/config/SOFTWARE")
        keys = self.rec(reg.root(),self.reg_key)
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
        keys = self.rec(reg.root(),self.reg_key)
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
        keys = self.rec(reg.root(),self.reg_key)
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
            if value.name() == self.reg_key:
                return {value.name(): [value.value(),str(key)[:-28]]}
                break
        return None 