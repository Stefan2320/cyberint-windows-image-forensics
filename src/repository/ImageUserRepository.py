from sqlalchemy.orm import Session
from src.repository.models  import ImageUser

class ImageUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, image_id: int, user_value: str) -> ImageUser:
        image_user = ImageUser(image_id=image_id, user_value=user_value)
        self.session.add(image_user)
        self.session.commit()
        return image_user
    
    def add_user_set(self, image_id: int, user_set):
        for user in user_set:
            self.add_user(image_id, user)

    def get_user(self, user_id: int) -> ImageUser:
        return self.session.query(ImageUser).filter_by(user_id=user_id).first()

    def get_users_by_image(self, image_id: int) -> list:
        return self.session.query(ImageUser).filter_by(image_id=image_id).all()

    def delete_user(self, user_id: int) -> None:
        image_user = self.session.query(ImageUser).filter_by(user_id=user_id).first()
        if image_user:
            self.session.delete(image_user)
            self.session.commit()

    def update_user(self, user_id: int, user_value: str) -> ImageUser:
        image_user = self.session.query(ImageUser).filter_by(user_id=user_id).first()
        if image_user:
            image_user.user_value = user_value
            self.session.commit()
        return image_user
