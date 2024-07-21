from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .init import Base
'''

TODO move to models
'''

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
    ips = relationship('ImageIP', back_populates='windows_image')
    users = relationship('ImageUser', back_populates='windows_image')
    guids = relationship('ImageGUID', back_populates='windows_image')
    persistances = relationship('ImagePersistance', back_populates='windows_image')

class ImageFile(Base):
    __tablename__ = 'image_files'

    file_id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('windows_image.image_id'), nullable=False)
    path = Column(String, nullable=False)
    is_malicious = Column(Boolean, nullable=True)

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

class ImageIP(Base):
    __tablename__ = 'image_ips'

    ip_id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('windows_image.image_id'), nullable=False)
    interface = Column(String, nullable=False)
    DhcpIPAddress = Column(String, nullable=True)
    DhcpServer = Column(String, nullable=True)
    DhcpNameServer = Column(String, nullable=True)
    IPAddress = Column(String, nullable=True)

    windows_image = relationship('WindowsImage', back_populates='ips')

class ImageUser(Base):
    __tablename__ = 'image_users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('windows_image.image_id'), nullable=False)
    user_value = Column(String, nullable=False)

    windows_image = relationship('WindowsImage', back_populates='users')

class ImageGUID(Base):
    __tablename__ = 'image_guids'

    guid_id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('windows_image.image_id'), nullable=False)
    guid_value = Column(String, nullable=False)

    windows_image = relationship('WindowsImage', back_populates='guids')

    
class ImagePersistance(Base):
    __tablename__ = 'image_persistance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('windows_image.image_id'), nullable=False)
    name = Column(String, nullable=True)
    path = Column(String, nullable=False)
    persistance_type = Column(String, nullable=False)
 
    
    windows_image = relationship('WindowsImage', back_populates='persistances')