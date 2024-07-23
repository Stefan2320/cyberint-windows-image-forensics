from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.repository.init import Base


class WindowsImage(Base):
    """
    Represents a Windows image in the database, containing metadata and relationships to related entities.

    This class defines the `windows_image` table and its attributes:
    - `image_id`: Primary key for the table, auto-incremented.
    - `image_name`: Name of the Windows image.
    """
    __tablename__ = 'windows_image'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    image_name = Column(String, nullable=False)

    files = relationship('ImageFile', back_populates='windows_image')
    hosts = relationship('ImageHost', back_populates='windows_image')
    ips = relationship('ImageIP', back_populates='windows_image')
    users = relationship('ImageUser', back_populates='windows_image')
    guids = relationship('ImageGUID', back_populates='windows_image')
    persistences = relationship('FilePersistence', back_populates='windows_image')