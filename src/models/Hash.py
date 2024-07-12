from abc import ABC, abstractmethod


class Hasher(ABC):
    @abstractmethod
    def compute_hash(self, path: str) -> str:
        pass

    @abstractmethod
    def get_hash_type(self) -> str:
        pass
