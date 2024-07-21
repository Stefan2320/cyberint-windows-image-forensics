from sqlalchemy.orm import Session
from src.repository.models import ImageHost

class ImageHostRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_host(self, image_id: int, host_name: str) -> ImageHost:
        image_host = ImageHost(image_id=image_id, host_name=host_name)
        self.session.add(image_host)
        self.session.commit()
        return image_host

    def add_host_set(self, image_id: int, host_set):
        for  host in host_set:
            self.add_host(image_id, host)

    def get_hosts_by_image_id(self, image_id: int):
        return self.session.query(ImageHost).filter(ImageHost.image_id == image_id).all()
