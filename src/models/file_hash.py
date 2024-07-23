from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.repository.init import Base


class FileHash(Base):
    """
    Represents a file hash entry in the database.

    This class defines the `file_hash` table and its attributes:
    - `hash_id`: Primary key for the table, auto-incremented.
    - `file_id`: Foreign key linking to the `image_files` table.
    - `hash_type`: Type of the hash (e.g., 'md5', 'sha256').
    - `hash_value`: The actual hash value.
    """
    __tablename__ = 'file_hash'

    hash_id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey('image_files.file_id'), nullable=False)
    hash_type = Column(String, nullable=False)
    hash_value = Column(String, nullable=False)

    image_file = relationship('ImageFile', back_populates='hashes')