from sqlalchemy.orm import Session
from src.models.file_hash import FileHash
from sqlalchemy.exc import SQLAlchemyError

class FileHashTable:
    def __init__(self, session: Session):
        self.session = session

    def add_hash(self, file_id: int, hash_type: str, hash_value: str) -> FileHash:
        """
        Adds a new hash entry to the database.
        """
        try:
            file_hash = FileHash(file_id=file_id, hash_type=hash_type, hash_value=hash_value)
            self.session.add(file_hash)
            self.session.commit()
            return file_hash
        except SQLAlchemyError as e:
            self.session.rollback()  
            print(f"Error adding hash to database: {e}")

    def get_hashes_by_file_id(self, file_id: int) -> list[FileHash]:
        """
        Retrieves all hashes associated with a given file ID.

        Returns:
            list[FileHash]: A list of FileHash instances associated with the specified file ID.
        """
        return self.session.query(FileHash).filter(FileHash.file_id == file_id).all()
