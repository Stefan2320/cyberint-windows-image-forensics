from sqlalchemy import Column, Integer, String, Boolean
from .init import Base

class FileModel(Base):
    '''
    Even if we have two hashes we pnly need one is_malicious because they will link to the same file
    TODO add name and path
    '''
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    path = Column(String, index=True)
    md5hash = Column(String, index=True)
    sha1hash = Column(String, index=True)
    is_malicious = Column(Boolean, default=None, nullable=True) 
