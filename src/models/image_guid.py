from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.repository.init import Base


class ImageGUID(Base):
    """
    Represents a GUID associated with a Windows image.

    This class defines the `image_guids` table and its attributes:
    - `guid_id`: Primary key for the table, auto-incremented.
    - `image_id`: Foreign key linking to the `windows_image` table.
    - `guid_value`: The GUID value associated with the Windows image.
    """
    __tablename__ = 'image_guids'

    guid_id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('windows_image.image_id'), nullable=False)
    guid_value = Column(String, nullable=False)

    windows_image = relationship('WindowsImage', back_populates='guids')
