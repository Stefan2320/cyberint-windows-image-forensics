from sqlalchemy.orm import Session
from src.repository.models import ImageGUID

class ImageGUIDRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_guid(self, image_id: int, guid_value: str) -> ImageGUID:
        image_guid = ImageGUID(image_id=image_id, guid_value=guid_value)
        self.session.add(image_guid)
        self.session.commit()
        return image_guid

    def get_guid(self, guid_id: int) -> ImageGUID:
        return self.session.query(ImageGUID).filter_by(guid_id=guid_id).first()

    def get_guids_by_image(self, image_id: int) -> list:
        return self.session.query(ImageGUID).filter_by(image_id=image_id).all()

    def delete_guid(self, guid_id: int) -> None:
        image_guid = self.session.query(ImageGUID).filter_by(guid_id=guid_id).first()
        if image_guid:
            self.session.delete(image_guid)
            self.session.commit()

    def update_guid(self, guid_id: int, guid_value: str) -> ImageGUID:
        image_guid = self.session.query(ImageGUID).filter_by(guid_id=guid_id).first()
        if image_guid:
            image_guid.guid_value = guid_value
            self.session.commit()
        return image_guid
