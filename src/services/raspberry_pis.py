from src.domain.config_loader import ConfigLoader
from src.services import Handler


class GetAllRaspberries(Handler):

    def handle(self):
        with self.manager.start() as uow:
            raspberries = uow.raspberry_pis.get_all()

        return raspberries

class AddRaspberryPiHandler(Handler):

    def handle(self, body):
        config_loader = ConfigLoader()
        objects = config_loader.translate_config(body)
        with self.manager.start() as uow:
            uow.raspberry_pis.add_raspberry_pi(objects)


class GetSingleRaspberryPiHandler(Handler):
    def handle(self, raspberry_id = None):
        with self.manager as uow:
            raspberry = uow.raspberry_pis.get_by_id(raspberry_id)

        return raspberry
