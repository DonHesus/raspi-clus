from services.raspberry_pis import AddRaspberryPiHandler
from tests.utilities import MockManager


def test_add_raspberry_pi():
    manager = MockManager()
    handler = AddRaspberryPiHandler(manager)
    handler.handle({"name": "RPI2", "address": "192.168.50.11", "mac_address": "41ab2a7c8a"})
