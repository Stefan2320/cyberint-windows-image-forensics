from sqlalchemy.orm import Session
from src.models.file_persistance import FilePersistence
from sqlalchemy.exc import SQLAlchemyError

class FilePersistenceTable:
    def __init__(self, session: Session):
        self.session = session

    def add_persistence(self, image_id: int, name: str, path: str, persistence_type: str) -> FilePersistence:
        """
        Adds a new persistence entry to the database.

        Args:
            image_id (int): The ID of the associated image.
            name (str): The name of the file with persistence.
            path (str): The path related to the file with persistence.
            persistence_type (str): The type of persistence (e.g., 'run', 'runOnce').
        """
        try:
            persistence = FilePersistence(
                image_id=image_id,
                name=name,
                path=path,
                persistence_type=persistence_type
            )
            self.session.add(persistence)
            self.session.commit()
            return persistence
        except SQLAlchemyError as e:
            self.session.rollback()  
            print(f"Error adding persistence to database: {e}") 

    def add_persistence_list(self, image_id: int, persistence_list: list, persistence_type: str) -> None:
        """
        Adds a list of persistence items to the database. Handles different persistence types differently.

        Notes:
            If persistence_type is 'run' or 'runOnce', expects a list of tuples with (name, path).
            For other types, expects a list of filenames with 'path' set to 'None'.
        """
        if persistence_type in {'run', 'runOnce'}:
            for reg_item in persistence_list:
                for name,path in reg_item.items():
                    if '\\' in name:
                        name, path = path, name
                    self.add_persistence(image_id=image_id, name=name, path=path, persistence_type=persistence_type)
        else:
            for filename in persistence_list:
                self.add_persistence(image_id, name=filename, path='None', persistence_type=persistence_type)

    def get_persistence(self, id: int) -> FilePersistence:
        """
        Retrieves a persistence entry by its ID.
        """
        return self.session.query(FilePersistence).filter_by(id=id).first()

    def get_persistence_by_image(self, image_id: int) -> list[FilePersistence]:
        """
        Retrieves all persistence entries associated with a given image ID.
        """
        return self.session.query(FilePersistence).filter_by(image_id=image_id).all()

    def delete_persistence(self, id: int) -> None:
        """
        Deletes a persistence entry by its ID.
        """
        persistence = self.session.query(FilePersistence).filter_by(id=id).first()
        if persistence:
            self.session.delete(persistence)
            self.session.commit()

    def update_persistence(self, id: int, name: str, path: str, persistence_type: str) -> FilePersistence:
        """
        Updates an existing persistence entry by its ID.
        """
        persistence = self.session.query(FilePersistence).filter_by(id=id).first()
        if persistence:
            persistence.name = name
            persistence.path = path
            persistence.persistence_type = persistence_type
            self.session.commit()
        return persistence
