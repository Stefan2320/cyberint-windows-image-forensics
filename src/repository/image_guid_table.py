from sqlalchemy.orm import Session
from src.models.image_guid import ImageGUID
from sqlalchemy.exc import SQLAlchemyError


class ImageGUIDTable:
    def __init__(self, session: Session):
        self.session = session

    def add_guid(self, image_id: int, guid_value: str) -> ImageGUID:
        """
        Adds a new GUID entry to the database.
        """
        try:
            image_guid = ImageGUID(image_id=image_id, guid_value=guid_value)
            self.session.add(image_guid)
            self.session.commit()
            return image_guid
        except SQLAlchemyError as e:
            self.session.rollback()  
            print(f"Error adding GUID to database: {e}")

    def get_guid(self, guid_id: int) -> ImageGUID:
        """
        Retrieves a GUID by its ID.
        """
        return self.session.query(ImageGUID).filter_by(guid_id=guid_id).first()

    def get_guids_by_image(self, image_id: int) -> list:
        """
        Retrieves all GUIDs associated with a given image ID.
        """
        return self.session.query(ImageGUID).filter_by(image_id=image_id).all()

    def delete_guid(self, guid_id: int) -> None:
        """
        Deletes a GUID by its ID.
        """
        image_guid = self.session.query(ImageGUID).filter_by(guid_id=guid_id).first()
        if image_guid:
            self.session.delete(image_guid)
            self.session.commit()

    def update_guid(self, guid_id: int, guid_value: str) -> ImageGUID:
        """
        Updates the value of a GUID by its ID.
        """
        image_guid = self.session.query(ImageGUID).filter_by(guid_id=guid_id).first()
        if image_guid:
            image_guid.guid_value = guid_value
            self.session.commit()
        return image_guid

