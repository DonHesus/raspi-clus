import uuid

from domain.models import RaspberryPi
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
        body["raspberry_id"] = uuid.uuid4()
        with self.manager.start() as uow:
            uow.raspberry_pis.add_raspberry_pi(RaspberryPi(**body))
            add_new_node(body)


class GetSingleRaspberryPiHandler(Handler):
    def handle(self, mac_address=None):
        with self.manager.start() as uow:
            raspberry = uow.raspberry_pis.get_by_mac_address(mac_address)

        return raspberry.as_dict()


class ChangeOSHandler(Handler):
    def handle(self, raspberry_id, os_id):
        with self.manager.start() as uow:
            raspberry_obj = uow.raspberry_pis.get_by_id(raspberry_id)
            RaspberryPi(raspberry_obj.name, raspberry_obj.address, raspberry_id.operating_system_id).change_os()
            uow.raspberry_pis.update_raspberry_system(raspberry_id, os_id)
