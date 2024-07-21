from sqlalchemy.orm import Session
from src.repository.models import ImageFile

class ImageFileRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_file(self, image_id: int, path: str,is_malicious: bool) -> ImageFile:
        image_file = ImageFile(image_id=image_id, path=path,is_malicious=is_malicious)
        self.session.add(image_file)
        self.session.commit()
        return image_file

    def get_files_by_image_id(self, image_id: int):
        return self.session.query(ImageFile).filter(ImageFile.image_id == image_id).all()
