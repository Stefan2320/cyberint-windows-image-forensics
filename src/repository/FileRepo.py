from sqlalchemy.orm import Session
from .models import FileModel

class FileRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_unknown_files(self) -> bool:
        return self.session.query(FileModel).filter(FileModel.is_malicious == None).all()