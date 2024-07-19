from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
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

class WindowsImage(Base):
    __tablename__ = 'windows_image'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    image_name = Column(String, nullable=False)

    files = relationship('ImageFile', back_populates='windows_image')
    hosts = relationship('ImageHost', back_populates='windows_image')

class ImageFile(Base):
    __tablename__ = 'image_files'

    file_id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('windows_image.image_id'), nullable=False)
    path = Column(String, nullable=False)

    # Relationships
    windows_image = relationship('WindowsImage', back_populates='files')
    hashes = relationship('FileHash', back_populates='image_file')

class FileHash(Base):
    __tablename__ = 'file_hash'

    hash_id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey('image_files.file_id'), nullable=False)
    hash_type = Column(String, nullable=False)
    hash_value = Column(String, nullable=False)

    image_file = relationship('ImageFile', back_populates='hashes')

class ImageHost(Base):
    __tablename__ = 'image_hosts'

    hosts_id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('windows_image.image_id'), nullable=False)
    host_name = Column(String, nullable=False)

    windows_image = relationship('WindowsImage', back_populates='hosts')