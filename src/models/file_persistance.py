from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from src.repository.init import Base

    
class FilePersistence(Base):
    """
    Represents a file persistence entry in the database.

    This class defines the `file_persistence` table and its attributes:
    - `id`: Primary key for the table, auto-incremented.
    - `image_id`: Foreign key linking to the `windows_image` table.
    - `name`: Optional name of the persistence entry.
    - `path`: The file path associated with the file that has persistence. Depending on the persistence_type it can be NULL.
    - `persistence_type`: Type of persistence ('runOnce', 'run', 'system','user').
    """
    __tablename__ = 'file_persistence'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('windows_image.image_id'), nullable=False)
    name = Column(String, nullable=True)
    path = Column(String, nullable=False)
    persistence_type = Column(String, nullable=False)
 
    
    windows_image = relationship('WindowsImage', back_populates='persistences')