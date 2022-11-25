import uuid
from ipaddress import ip_address
from typing import List


class OperatingSystem:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def serialize(self):
        pass


class Cluster:
    """Allows to manage entire cluster"""

    raspberry_pis: List['RaspberryPi'] = []
    cluster_id: uuid.UUID = None

    def __init__(self, name: str, network: ip_address, raspberry_pis: List['RaspberryPi'] = None,
                 cluster_id: uuid.UUID = None):
        self.cluster_id = cluster_id if not None else self.cluster_id
        self.name = name
        self.network = network
        self.raspberry_pis = raspberry_pis if not None else self.raspberry_pis

    def change_os(self, operating_system: OperatingSystem, raspberry_pi: 'RaspberryPi'):
        raise NotImplementedError()

    def serialize(self):
        pass


class RaspberryPi:

    operating_system: OperatingSystem = None

    def __init__(self, name, address: ip_address, operating_system: OperatingSystem = None, cluster: Cluster = None,
                 raspberry_id: uuid.UUID = None):
        self.name = name
        self.address = address
        self.operating_system = operating_system if not None else self.operating_system
        self.cluster = cluster

    def change_os(self, operating_system: OperatingSystem):
        raise NotImplementedError()

    def serialize(self):
        pass
