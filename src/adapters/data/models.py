import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

db = SQLAlchemy()


class OperatingSystem(db.Model):
    __tablename__ = "operating_systems"

    id = Column(UUIDType, primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    path = Column(String, nullable=False)
    raspberry_pis = relationship("RaspberryPi", backref="OS")


class Cluster(db.Model):

    __tablename__ = "clusters"

    id = Column(UUIDType, primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    network = Column(String, nullable=False)

    raspberry_pis = relationship('RaspberryPi', backref='cluster')


class RaspberryPi(db.Model):

    __tablename__ = "raspberry_pis"

    id = Column(UUIDType, primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    address = Column(String, nullable=False)
    operating_system_id = Column(UUIDType, ForeignKey("operating_systems.id"))
    cluster_id = Column(UUIDType, ForeignKey('clusters.id'))
