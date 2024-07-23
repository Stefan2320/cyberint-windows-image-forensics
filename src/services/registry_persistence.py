from Registry import Registry
from src.services.registry_extractor import Extractor


class RegistryPersistence(Extractor):
    reg_keys = [
        r"\Microsoft\Windows\CurrentVersion\Run",
        r"\Microsoft\Windows\CurrentVersion\RunOnce"
    ]

    def __init__(self, keyword: str = None) -> None:
        """
        Initializes the RegistryPersistence with an optional keyword.
        """
        super().__init__(keyword)

    def extract(self, location: str, registry_key: str, registry_hive: str = None) -> list[dict[str, list[str]]]:
        """
        Extracts registry values from a specified location and key.

        Args:
            location (str): The location of the equivalent C: on the mounted Windows image.
            registry_key (str): The registry key to extract.
            registry_hive (str, optional): The registry hive to use.

        Returns:
            list[dict[str, list[str]]]: A list of dictionaries containing registry values and their paths.
        """
        self.hosts = []
        reg = Registry.Registry(location + registry_hive)
        keys = self.rec(reg.root(), registry_key)
        for subkey in keys:
            key = reg.open(subkey[5:])
            for value in key.values():
                if value.value_type() in (Registry.RegSZ, Registry.RegExpandSZ):
                    self.hosts.append({value.name(): [value.value(), str(key)[:-28]]})
        return self.hosts

    def extract_run_key(self, location: str) -> list[dict[str, str]]:
        """
        Extracts values from the Run registry key.

        Returns:
            list[dict[str, str]]: A list of dictionaries containing names and file paths from the Run key.
        """
        registry_result = self.extract(location, self.reg_keys[0], r"/Windows/System32/config/SOFTWARE")
        persistance_files = []
        for reg_item in registry_result:
            for name, value in reg_item.items():
                file_path = value[0]
                persistance_files.append({name: file_path})
        return persistance_files

    def extract_runOnce_key(self, location: str) -> list[dict[str, str]]:
        """
        Extracts values from the RunOnce registry key.

        Returns:
            list[dict[str, str]]: A list of dictionaries containing names and file paths from the RunOnce key.
        """
        registry_result = self.extract(location, self.reg_keys[1], r"/Windows/System32/config/SOFTWARE")
        persistance_files = []
        for reg_item in registry_result:
            for name, value in reg_item.items():
                file_path = value[0]
                persistance_files.append({name: file_path})
        return persistance_files
