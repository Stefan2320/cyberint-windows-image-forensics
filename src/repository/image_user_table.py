from sqlalchemy.orm import Session
from src.models.image_user import ImageUser
from sqlalchemy.exc import SQLAlchemyError


class ImageUserTable:
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, image_id: int, user_value: str) -> ImageUser:
        """
        Adds a new user entry to the database.
        """
        try:
            image_user = ImageUser(image_id=image_id, user_value=user_value)
            self.session.add(image_user)
            self.session.commit()
            return image_user
        except SQLAlchemyError as e:
            self.session.rollback() 
            print(f"Error adding user to database: {e}") 

    def add_user_set(self, image_id: int, user_set: set) -> None:
        """
        Adds a set of user entries to the database.
        """
        for user in user_set:
            print(user)
            self.add_user(image_id, user)

    def get_user(self, user_id: int) -> ImageUser:
        """
        Retrieves a user entry by its ID.
        """
        return self.session.query(ImageUser).filter_by(user_id=user_id).first()

    def get_users_by_image(self, image_id: int) -> list:
        """
        Retrieves all user entries associated with a given image ID.
        """
        return self.session.query(ImageUser).filter_by(image_id=image_id).all()

    def delete_user(self, user_id: int) -> None:
        """
        Deletes a user entry by its ID.
        """
        image_user = self.session.query(ImageUser).filter_by(user_id=user_id).first()
        if image_user:
            self.session.delete(image_user)
            self.session.commit()

    def update_user(self, user_id: int, user_value: str) -> ImageUser:
        """
        Updates an existing user entry.
        """
        image_user = self.session.query(ImageUser).filter_by(user_id=user_id).first()
        if image_user:
            image_user.user_value = user_value
            self.session.commit()
        return image_user
