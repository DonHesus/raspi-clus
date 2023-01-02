import uuid

from domain.models import OperatingSystem
from src.domain.config_loader import ConfigLoader
from src.services import Handler


class GetAllOperatingSystems(Handler):

    def handle(self):
        with self.manager.start() as uow:
            oses = uow.operating_systems.get_all()

            oses_list = [os.as_dict() for os in oses]
        return oses_list

class AddOperatingSystemHandler(Handler):

    def handle(self, body):
        body["os_id"] = uuid.uuid4()
        with self.manager.start() as uow:
            system_os = OperatingSystem(**body)
            uow.operating_systems.add_operating_system(system_os)


class GetSingleOperatingSystemHandler(Handler):
    def handle(self, os_id = None):
        with self.manager.start() as uow:
            operating_system = uow.operating_systems.get_by_id(os_id)

        return operating_system.as_dict()
