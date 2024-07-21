from sqlalchemy.orm import Session
from src.repository.models import ImageIP

class ImageIPRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_ip(self, image_id: int, interface: str, 
               DhcpIPAddress: str = None, 
               DhcpServer: str = None, 
               DhcpNameServer: str = None, 
               IPAddress: str = None) -> ImageIP:
        '''
        add rollbacks
        '''
        image_ip = ImageIP(
            image_id=image_id,
            interface=interface,
            DhcpIPAddress=DhcpIPAddress,
            DhcpServer=DhcpServer,
            DhcpNameServer=DhcpNameServer,
            IPAddress=IPAddress
        )
        self.session.add(image_ip)
        self.session.commit()
        return image_ip

    def add_ip_set(self, image_id: int, ips: dict):
            """Add a set of IP records to the database."""
            for interface, properties in ips.items():
                interface = self.clean_interface(interface)
                properties = self.extract_properties(properties)
                self.add_ip(image_id, interface, **properties)

    def clean_interface(self, interface: str) -> str:
        """Clean up the IP interface string."""
        return interface.strip('{}')

    def extract_properties(self, properties: list) -> dict:
        """Extract IP properties from a list of dictionaries."""
        ip_properties = {
            'DhcpIPAddress': None,
            'DhcpServer': None,
            'DhcpNameServer': None,
            'IPAddress': None
        }
        ip_dict = {}
        if isinstance(properties, list):
            for property_set in properties:
                if isinstance(property_set, set) and len(property_set) == 2:
                    key, value = list(property_set)
                    if key in ip_properties:
                        ip_dict[key] = value 
                    if value in ip_properties:
                        ip_dict[value] = key

        return ip_dict 

    def get_ip(self, id: int) -> ImageIP:
        return self.session.query(ImageIP).filter_by(id=id).first()

    def get_ips_by_image(self, image_id: int) -> list:
        return self.session.query(ImageIP).filter_by(image_id=image_id).all()

    def delete_ip(self, id: int) -> None:
        image_ip = self.session.query(ImageIP).filter_by(id=id).first()
        if image_ip:
            self.session.delete(image_ip)
            self.session.commit()

    def update_ip(self, id: int, 
                  interface: str = None, 
                  DhcpIPAddress: str = None, 
                  DhcpServer: str = None, 
                  DhcpNameServer: str = None, 
                  IPAddress: str = None) -> ImageIP:
        image_ip = self.session.query(ImageIP).filter_by(id=id).first()
        if image_ip:
            if interface is not None:
                image_ip.interface = interface
            if DhcpIPAddress is not None:
                image_ip.DhcpIPAddress = DhcpIPAddress
            if DhcpServer is not None:
                image_ip.DhcpServer = DhcpServer
            if DhcpNameServer is not None:
                image_ip.DhcpNameServer = DhcpNameServer
            if IPAddress is not None:
                image_ip.IPAddress = IPAddress
            self.session.commit()
        return image_ip