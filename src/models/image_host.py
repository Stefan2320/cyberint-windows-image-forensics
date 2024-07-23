from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.repository.init import Base


class ImageHost(Base):
    """
    Represents a host associated with a Windows image in the database.

    This class defines the `image_hosts` table and its attributes:
    - `hosts_id`: Primary key for the table, auto-incremented.
    - `image_id`: Foreign key linking to the `windows_image` table.
    - `host_name`: The name of the host associated with the Windows image.
    """
    __tablename__ = 'image_hosts'

    hosts_id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('windows_image.image_id'), nullable=False)
    host_name = Column(String, nullable=False)

    windows_image = relationship('WindowsImage', back_populates='hosts')