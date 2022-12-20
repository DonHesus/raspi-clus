from src.domain.config_loader import ConfigLoader
from src.services import Handler


class GetAllOperatingSystems(Handler):

    def handle(self):
        with self.manager.start() as uow:
            oses = uow.operating_systems.get_all()

        return oses

class AddOperatingSystemHandler(Handler):

    def handle(self, body):
        config_loader = ConfigLoader()
        objects = config_loader.translate_config(body)
        with self.manager.start() as uow:
            uow.operating_systems.add_operating_system(objects)


class GetSingleOperatingSystemHandler(Handler):
    def handle(self, os_id = None):
        with self.manager as uow:
            operating_system = uow.operating_systems.get_by_id(os_id)

        return operating_system
