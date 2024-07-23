from sqlalchemy.orm import Session
from src.models.image_host import ImageHost
from sqlalchemy.exc import SQLAlchemyError


class ImageHostTable:
    def __init__(self, session: Session):
        self.session = session

    def add_host(self, image_id: int, host_name: str) -> ImageHost:
        """
        Adds a new host entry to the database.
        """
        try:
            image_host = ImageHost(image_id=image_id, host_name=host_name)
            self.session.add(image_host)
            self.session.commit()
            return image_host
        except SQLAlchemyError as e:
            self.session.rollback()  
            print(f"Error adding host to database: {e}")   
            
    def add_host_set(self, image_id: int, host_set: set) -> None:
        """
        Adds a set of hosts to the database.
        """
        for host in host_set:
            self.add_host(image_id, host)

    def get_hosts_by_image_id(self, image_id: int) -> list[ImageHost]:
        """
        Retrieves all hosts associated with a given image ID.

        Returns:
            List[ImageHost]: A list of ImageHost instances associated with the specified image ID.
        """
        return self.session.query(ImageHost).filter(ImageHost.image_id == image_id).all()
