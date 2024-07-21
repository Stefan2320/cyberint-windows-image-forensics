from sqlalchemy.orm import Session
from src.repository.models import WindowsImage

class WindowsImageRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_image(self, image_name: str) -> WindowsImage:
        windows_image = WindowsImage(image_name=image_name)
        self.session.add(windows_image)
        self.session.commit()
        return windows_image

    def get_image_by_id(self, image_id: int) -> WindowsImage:
        return self.session.query(WindowsImage).filter(WindowsImage.image_id == image_id).first()
