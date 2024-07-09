from abc import ABC, abstractmethod


class Hasher(ABC):
    @abstractmethod
    def compute_hash(self, path: str) -> str:
        pass
