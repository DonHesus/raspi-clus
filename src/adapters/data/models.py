import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType, ChoiceType

db = SQLAlchemy()

OS_TYPES = [
    (u'golden', u'Golden'),
    (u'distributed', u'Distributed'),

]


class OperatingSystem(db.Model):
    __tablename__ = "operating_systems"

    id = Column(UUIDType, primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    path = Column(String, nullable=False)
    os_type = Column(ChoiceType(OS_TYPES), nullable=False)
    raspberry_pis = relationship("RaspberryPi", backref="OS")
    golden_image_id = Column(UUIDType, nullable=True)

    def as_dict(self):
        return {"id": self.id,
                "name": self.name,
                "path": self.path,
                "os_type": self.os_type.value,
                "raspberry_pis": [raspberry.as_dict() for raspberry in self.raspberry_pis],
                "golden_image_id": self.golden_image_id
                }


class Cluster(db.Model):

    __tablename__ = "clusters"

    id = Column(UUIDType, primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    network = Column(String, nullable=False)

    raspberry_pis = relationship('RaspberryPi', backref='cluster')

    def as_dict(self):
        return {"id": self.id,
                "name": self.name,
                "network": self.network,
                "raspberry_pis": [raspberry.as_dict() for raspberry in self.raspberry_pis]}


class RaspberryPi(db.Model):

    __tablename__ = "raspberry_pis"

    id = Column(UUIDType, primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    address = Column(String, nullable=False)
    mac_address = Column(String, nullable=False)
    serial_number = Column(String, nullable=False)
    operating_system_id = Column(UUIDType, ForeignKey("operating_systems.id"))
    cluster_id = Column(UUIDType, ForeignKey('clusters.id'))
    last_alive = Column(DateTime, nullable=True)

    def as_dict(self):
        return {"id": self.id,
                "name": self.name,
                "address": self.address,
                "mac_address": self.mac_address,
                "serial_number": self.serial_number,
                "last_alive": str(self.last_alive),
                "operating_system_id": self.operating_system_id,
                "cluster_id": self.cluster_id}
