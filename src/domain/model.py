from ipaddress import ip_address


class OperatingSystem:
    pass


class Cluster:
    """Allows to manage entire cluster"""
    def __init__(self, name: str, network: ip_address):
        self.name = name
        self.network = network

    def change_os(self, os_name):
        raise NotImplementedError()


class RaspberryPi:

    def __init__(self, name, address: ip_address):
        self.name = name
        self.address = address
