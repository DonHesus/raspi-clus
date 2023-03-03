import uuid

from domain.models import RaspberryPi, OperatingSystem
from services.configs_manipulation import add_new_node

from src.services import Handler


class GetAllRaspberries(Handler):

    def handle(self):
        with self.manager.start() as uow:
            raspberries = uow.raspberry_pis.get_all()

        raspberries_list = [raspberry.as_dict() for raspberry in raspberries]
        return raspberries_list


class AddRaspberryPiHandler(Handler):

    def handle(self, body):
        body["id"] = uuid.uuid4()
        with self.manager.start() as uow:
            uow.raspberry_pis.add_raspberry_pi(RaspberryPi(**body))
            add_new_node(body)


class GetSingleRaspberryPiHandler(Handler):
    def handle(self, mac_address=None):
        with self.manager.start() as uow:
            raspberry = uow.raspberry_pis.get_by_mac_address(mac_address)

        return raspberry.as_dict()


class ChangeOSHandler(Handler):
    def handle(self, mac_address, os_id):
        with self.manager.start() as uow:
            raspberry_obj = uow.raspberry_pis.get_by_mac_address(mac_address)
            image_to_distribute = uow.operating_systems.get_by_id(os_id)
            new_image_id = uuid.uuid4()
            new_system = RaspberryPi(**raspberry_obj.as_dict())\
                .change_os(image_to_distribute=OperatingSystem(**image_to_distribute.as_dict()),
                           new_image_id=new_image_id)
            uow.operating_systems.add_operating_system(new_system)
            uow.raspberry_pis.update_raspberry_system(mac_address, new_image_id)


class RefreshOSHandler(Handler):
    def handle(self, mac_address):
        with self.manager.start() as uow:
            raspberry_obj = uow.raspberry_pis.get_by_mac_address(mac_address)
            image_to_distribute = uow.operating_systems.get_by_id(raspberry_obj.OS.golden_image_id)
            new_image_id = uuid.uuid4()
            new_system = RaspberryPi(**raspberry_obj.as_dict())\
                .change_os(image_to_distribute=OperatingSystem(**image_to_distribute.as_dict()),
                           new_image_id=new_image_id)
            uow.operating_systems.add_operating_system(new_system)
            uow.raspberry_pis.update_raspberry_system(mac_address, new_image_id)
