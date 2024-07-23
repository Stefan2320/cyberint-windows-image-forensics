from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.repository.init import Base


class ImageUser(Base):
    """
    Represents user-related information associated with a Windows image in the database.

    This class defines the `image_users` table and its attributes:
    - `user_id`: Primary key for the table, auto-incremented.
    - `image_id`: Foreign key linking to the `windows_image` table.
    - `user_value`: Value representing the users from a Windows image.
    """
    __tablename__ = 'image_users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('windows_image.image_id'), nullable=False)
    user_value = Column(String, nullable=False)

    windows_image = relationship('WindowsImage', back_populates='users')