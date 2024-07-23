from abc import ABC, abstractmethod
from Registry import Registry

class Extractor(ABC):
    """
    Abstract base class for extracting data from Windows registry files.

    Attributes:
        reg_key (str): The registry key to be used for extraction.
    """

    def __init__(self, reg_key: str = None):
        self.reg_key = reg_key

    @abstractmethod
    def extract(self, location: str):
        """
        Abstract method for extracting data from the registry.

        Args:
            location (str): The file path of the equivalent C: dir on the mounted image. 
        """
        pass

    def rec(self, key, reg_key: str, paths=None, depth=0):
        """
        Recursive helper method to collect paths matching a registry key.

        Args:
            key: The current registry key to inspect.
            reg_key (str): The registry key to match against (it's more like a keyword). 
            paths (list, optional): A list to store matched paths.
            depth (int, optional): The current recursion depth.

        Returns:
            list: A list of paths matching the registry key.
        """
        if paths is None:
            paths = []
        if reg_key in key.path():
            paths.append(key.path())
        for subkey in key.subkeys():
            self.rec(subkey, reg_key, paths, depth + 1)
        return paths

class GeneralExtractor(Extractor):
    """
    Extractor for general registry data.
    Not used but can be useful for extending the application.

    Attributes:
        location (str): The location of equivalent C: directory on the mounted image.
        reg_hive (str): The registry hive to be used.
    """

    def __init__(self, location: str = None, reg_hive: str = None, reg_key: str = None):
        super().__init__(reg_key)
        self.location = location
        self.reg_hive = reg_hive

    def extract(self) -> list:
        """
        Extracts data from the specified registry hive.

        Returns:
            list: A list of dictionaries containing registry values. Has the format [{'reg_key':['value','complete_reg_hive_path']}]
        """
        self.data = []
        reg = Registry.Registry(self.location + self.reg_hive)
        keys = self.rec(reg.root(), self.reg_key)
        for subkey in keys:
            key = reg.open(subkey[5:])
            for value in [v for v in key.values()
                          if v.value_type() in {Registry.RegSZ, Registry.RegExpandSZ}]:
                self.data.append({value.name(): [value.value(), str(key)[:-28]]})
        return self.data

class UserExtractor(Extractor):
    """
    Extractor for user-related data from the registry.
    """

    def extract(self, location: str) -> list: 
        self.users = []
        reg = Registry.Registry(f"{location}/Windows/System32/config/SOFTWARE")
        keys = self.rec(reg.root(), self.reg_key)
        for subkey in keys:
            key = reg.open(subkey[5:])
            for value in [v for v in key.values()
                          if v.value_type() in {Registry.RegSZ, Registry.RegExpandSZ}]:
                self.users.append({value.name(): [value.value(), str(key)[:-28]]})
        return self.users

    def set_reg_key(self, key: str) -> None:
        self.reg_key = key

class HostExtractor(Extractor):
    """
    Extractor for host-related data from the registry.
    """

    def extract(self, location: str) -> list:
        self.hosts = []
        reg = Registry.Registry(f"{location}/Windows/System32/config/SYSTEM")
        keys = self.rec(reg.root(), self.reg_key)
        for subkey in keys:
            key = reg.open(subkey[5:])
            for value in [v for v in key.values()
                          if v.value_type() in {Registry.RegSZ, Registry.RegExpandSZ}]:
                self.hosts.append({value.name(): [value.value(), str(key)[:-28]]})
        return self.hosts

    def set_reg_key(self, key: str) -> None:
        self.reg_key = key

class IPExtractor(Extractor):
    """
    Extractor for IP-related data from the registry.
    """

    def extract(self, location: str) -> list:
        self.ip = []
        reg = Registry.Registry(f"{location}/Windows/System32/config/SYSTEM")
        keys = self.rec(reg.root(), self.reg_key)
        for subkey in keys:
            key = reg.open(subkey[5:])
            for value in [v for v in key.values()
                          if v.value_type() in {Registry.RegSZ, Registry.RegExpandSZ}]:
                self.ip.append({value.name(): [value.value(), str(key)[:-28]]})
        return self.ip

    def set_reg_key(self, key: str) -> None:
        self.reg_key = key

class GUIDExtractor(Extractor):
    """
    Extractor for GUID-related data from the registry.
    """

    def extract(self, location: str) -> list:
        reg = Registry.Registry(f"{location}/Windows/System32/config/SOFTWARE")
        key = reg.open("Microsoft\\Cryptography")
        for value in [v for v in key.values()
                      if v.value_type() in {Registry.RegSZ, Registry.RegExpandSZ}]:
            if value.name() == self.reg_key:
                return {value.name(): [value.value(), str(key)[:-28]]}
        return None

    def set_reg_key(self, key: str) -> None:
        self.reg_key = key
