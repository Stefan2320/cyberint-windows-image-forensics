from sqlalchemy.orm import Session
from src.repository.models import ImagePersistance

class ImagePersistanceRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_persistence(self, image_id: int, name: str, path: str, persistence_type: str) -> ImagePersistance:
        persistence = ImagePersistance(image_id=image_id, name=name, path=path, persistance_type=persistence_type)
        self.session.add(persistence)
        self.session.commit()
        return persistence

    def add_persistence_list(self, image_id: int, persistence_list: list, persistence_type: str):
        if persistence_type == 'run' or persistence_type == 'runOnce':
            for reg_item in persistence_list:
                name, path = list(reg_item)
                if '\\' in name:
                    name, path = path, name
                self.add_persistence(image_id=image_id, name=name, path=path,persistence_type=persistence_type)
        else: 
            for filename in persistence_list:
                self.add_persistence(image_id, name=filename, path='None', persistence_type=persistence_type)

    def get_persistence(self, id: int) -> ImagePersistance:
        return self.session.query(ImagePersistance).filter_by(id=id).first()

    def get_persistence_by_image(self, image_id: int) -> list:
        return self.session.query(ImagePersistance).filter_by(image_id=image_id).all()

    def delete_persistence(self, id: int) -> None:
        persistence = self.session.query(ImagePersistance).filter_by(id=id).first()
        if persistence:
            self.session.delete(persistence)
            self.session.commit()

    def update_persistence(self, id: int, name: str, path: str, persistence_type: str) -> ImagePersistance:
        persistence = self.session.query(ImagePersistance).filter_by(id=id).first()
        if persistence:
            persistence.name = name
            persistence.path = path
            persistence.persistence_type = persistence_type
            self.session.commit()
        return persistence
