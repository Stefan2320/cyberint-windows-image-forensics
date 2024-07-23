from sqlalchemy.orm import Session
from src.models.image_file import ImageFile
from sqlalchemy.exc import SQLAlchemyError


class ImageFileTable:
    def __init__(self, session: Session):
        self.session = session

    def add_file(self, image_id: int, path: str, is_malicious: bool) -> ImageFile:
        """
        Adds a new file entry to the database.
        """
        try:
            image_file = ImageFile(image_id=image_id, path=path, is_malicious=is_malicious)
            self.session.add(image_file)
            self.session.commit()
            return image_file
        except SQLAlchemyError as e:
            self.session.rollback() 
            print(f"Error adding file to database: {e}")

    def get_files_by_image_id(self, image_id: int) -> list[ImageFile]:
        """
        Retrieves all files associated with a given image ID.

        Returns:
            list[ImageFile]: A list of ImageFile instances associated with the specified image ID.
        """
        return self.session.query(ImageFile).filter(ImageFile.image_id == image_id).all()
