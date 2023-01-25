import uuid
import subprocess
from ipaddress import ip_address
from typing import List

from services.configs_manipulation import change_fstab_entry
from services.image_manipulation import create_new_distributed_image


class OperatingSystem:
    def __init__(self, name, path, os_type: str, os_id: uuid.UUID = None):
        self.name = name
        self.path = path
        self.os_id = os_id
        self.os_type = type

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
    alive: bool = None

    def __init__(self, name, address: ip_address, mac_address: str, serial_number: str,
                 operating_system_id: OperatingSystem = None,
                 cluster_id: uuid.UUID = None, raspberry_id: uuid.UUID = None):
        self.name = name
        self.address = address
        self.operating_system_id = operating_system_id if not None else self.operating_system_id
        self.cluster_id = cluster_id
        self.raspberry_id = raspberry_id if not None else self.raspberry_id
        self.mac_address = mac_address
        self.serial_number = serial_number

    def change_os(self, os_obj: OperatingSystem, new_os_obj: OperatingSystem):
        """
        """
        create_new_distributed_image()
        change_fstab_entry()
        self.reboot()



    def refresh_os(self):
        pass

    def reboot(self):
        pass

    def serialize(self):
        pass
