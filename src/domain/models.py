import uuid
from ipaddress import ip_address
from typing import List


class OperatingSystem:
    def __init__(self, name, path, os_id: uuid.UUID = None):
        self.name = name
        self.path = path
        self.os_id = os_id

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

    def change_os(self, operating_system: OperatingSystem):
        raise NotImplementedError()

    def serialize(self):
        pass


class RaspberryPi:

    operating_system_id: OperatingSystem = None
    raspberry_id: uuid.UUID = None
    alive : bool = None

    def __init__(self, name, address: ip_address, operating_system_id: OperatingSystem = None, cluster_id: uuid.UUID = None,
                 raspberry_id: uuid.UUID = None):
        self.name = name
        self.address = address
        self.operating_system_id = operating_system_id if not None else self.operating_system_id
        self.cluster_id = cluster_id
        self.raspberry_id = raspberry_id if not None else self.raspberry_id

    def change_os(self, os_obj: OperatingSystem):
        print("Changing OS")

    def serialize(self):
        pass
