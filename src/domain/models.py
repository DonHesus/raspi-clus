import uuid
from ipaddress import ip_address
from typing import List

import paramiko as paramiko

from services.communication import execute_ssh_raspberry_command, execute_server_command
from settings import Settings
from src.services.configs_manipulation import edit_fstab_conf, add_fstab_entry
from src.services.image_manipulation import create_new_distributed_image


class OperatingSystem:
    def __init__(self, name, path, os_type: str, id: uuid.UUID = None, golden_image_id: uuid.UUID = None,
                 raspberry_pis=None):
        self.name = name
        self.path = path
        self.os_id = id
        self.os_type = os_type
        self.raspberry_pis = raspberry_pis
        self.golden_image_id = golden_image_id

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
                 operating_system_id: OperatingSystem = None, last_alive = None,
                 cluster_id: uuid.UUID = None, id: uuid.UUID = None):
        self.name = name
        self.address = address
        self.operating_system_id = operating_system_id if not None else self.operating_system_id
        self.cluster_id = cluster_id
        self.raspberry_id = id if not None else self.raspberry_id
        self.mac_address = mac_address
        self.serial_number = serial_number
        self.last_alive = last_alive

    def change_os(self, image_to_distribute: OperatingSystem, new_image_id: uuid.UUID) -> OperatingSystem:
        image_path = create_new_distributed_image(image_to_distribute.path, new_image_id=new_image_id,
                                                  hostname=self.name)
        if self.operating_system_id:
            edit_fstab_conf(previous_os_id=self.operating_system_id, os_id=new_image_id)
            self._reboot()
            self._delete_previous_image()
        else:
            add_fstab_entry(os_id=new_image_id, raspberry_serial=self.serial_number, hostname=self.name)
        return OperatingSystem(name=image_to_distribute.name, os_type="distributed", id=new_image_id,
                               path=image_path, golden_image_id=image_to_distribute.os_id)

    def refresh_os(self):
        pass

    def _reboot(self):
        execute_ssh_raspberry_command(command="/sbin/reboot -f > /dev/null 2>%1 %", address=self.address, username="pi",
                                      password="raspberry")

    def _delete_previous_image(self):
        execute_server_command(f"rm -rf {Settings.image_store}/{self.operating_system_id}")

    def serialize(self):
        pass
