from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.repository.init import Base



class ImageFile(Base):
    """
    Represents a file associated with a Windows image in the database.

    This class defines the `image_files` table and its attributes:
    - `file_id`: Primary key for the table, auto-incremented.
    - `image_id`: Foreign key linking to the `windows_image` table.
    - `path`: Path to the file within the image.
    - `is_malicious`: Boolean indicating whether the file is considered malicious. If it's empty then the hash wasn't found. 
    """
    __tablename__ = 'image_files'

    file_id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('windows_image.image_id'), nullable=False)
    path = Column(String, nullable=False)
    is_malicious = Column(Boolean, nullable=True)

    windows_image = relationship('WindowsImage', back_populates='files')
    hashes = relationship('FileHash', back_populates='image_file')