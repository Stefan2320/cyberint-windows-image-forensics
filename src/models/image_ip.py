from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.repository.init import Base


class ImageIP(Base):
    """
    Represents IP information associated with a Windows image in the database.

    This class defines the `image_ips` table and its attributes:
    - `ip_id`: Primary key for the table, auto-incremented.
    - `image_id`: Foreign key linking to the `windows_image` table.
    - `interface`: Network interface name or identifier.
    - `DhcpIPAddress`: IP address assigned by DHCP, if available.
    - `DhcpServer`: DHCP server address, if available.
    - `DhcpNameServer`: DNS server address assigned by DHCP, if available.
    - `IPAddress`: Static IP address, if available.
    """
    __tablename__ = 'image_ips'

    ip_id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('windows_image.image_id'), nullable=False)
    interface = Column(String, nullable=False)
    DhcpIPAddress = Column(String, nullable=True)
    DhcpServer = Column(String, nullable=True)
    DhcpNameServer = Column(String, nullable=True)
    IPAddress = Column(String, nullable=True)

    windows_image = relationship('WindowsImage', back_populates='ips')
