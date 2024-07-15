from Registry import Registry
from src.models.Info_extractor import Extractor

class PersistenceCheckerRegistry(Extractor):

    reg_keys = [ r"\Microsoft\Windows\CurrentVersion\Run",
                 r"\Microsoft\Windows\CurrentVersion\RunOnce"]

    def __init__(self, keyword: str = None):
        super().__init__(keyword)

    def extract(self, location: str,registry_key: str, registry_hive: str = None):
        self.hosts = []
        reg = Registry.Registry(location+registry_hive)
        keys = self.rec(reg.root(),registry_key)
        for subkeys in keys: 
            key = reg.open(subkeys[5:])
            for value in [v for v in key.values() \
                            if v.value_type() == Registry.RegSZ or \
                                v.value_type() == Registry.RegExpandSZ]:
                self.hosts.append({value.name():[value.value(), str(key)[:-28]]})
        return self.hosts

    # TODO maybe refactor here everything, create an extractor and use it here
    def extract_run_key(self, location: str):
        return self.extract(location, self.reg_keys[0], r"/Windows/System32/config/SOFTWARE")

    def extract_runOnce_key(self, location: str):
        self.extract(location, self.reg_keys[1],r"/Windows/System32/config/SOFTWARE")

    def add_registry_keys(self, new_reg_key):
        self.reg_keys.append(new_reg_key)
        