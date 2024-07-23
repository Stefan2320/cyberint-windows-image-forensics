from sqlalchemy.orm import Session
from src.models.windows_image import WindowsImage
from sqlalchemy.exc import SQLAlchemyError


class WindowsImageTable:
    def __init__(self, session: Session):
        self.session = session

    def add_image(self, image_name: str) -> WindowsImage:
        """
        Adds a new Windows image entry to the database.
        """
        try:
            windows_image = WindowsImage(image_name=image_name)
            self.session.add(windows_image)
            self.session.commit()
            return windows_image
        except SQLAlchemyError as e:
            self.session.rollback()  
            print(f"Error adding Windows image to database: {e}") 

    def get_image_by_id(self, image_id: int) -> WindowsImage:
        """
        Retrieves a Windows image entry by its ID.
        """
        return self.session.query(WindowsImage).filter(WindowsImage.image_id == image_id).first()
