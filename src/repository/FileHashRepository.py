from sqlalchemy.orm import Session
from src.repository.models import FileHash

class FileHashRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_hash(self, file_id: int, hash_type: str, hash_value: str) -> FileHash:
        file_hash = FileHash(file_id=file_id, hash_type=hash_type, hash_value=hash_value)
        self.session.add(file_hash)
        self.session.commit()
        return file_hash

    def get_hashes_by_file_id(self, file_id: int):
        return self.session.query(FileHash).filter(FileHash.file_id == file_id).all()
