import uuid
from pathlib import Path

from domain.models import OperatingSystem
from services.image_manipulation import add_new_golden_image
from settings import Settings
from src.services import Handler


class GetAllOperatingSystems(Handler):

    def handle(self):
        with self.manager.start() as uow:
            oses = uow.operating_systems.get_all()

            oses_list = [os.as_dict() for os in oses]
        return oses_list


class AddOperatingSystemHandler(Handler):

    def handle(self, name, system_src, boot_src):
        os_id = uuid.uuid4()
        golden_image_path = Path(Settings.image_store) / "golden_images" / f"{os_id}"
        with self.manager.start() as uow:
            system_os = OperatingSystem(name=name, path=golden_image_path, os_id=os_id, os_type="golden")
            add_new_golden_image(system_files_path=system_src, boot_dir_path=boot_src)
            uow.operating_systems.add_operating_system(system_os)


class GetSingleOperatingSystemHandler(Handler):
    def handle(self, os_id=None):
        with self.manager.start() as uow:
            operating_system = uow.operating_systems.get_by_id(os_id)

        return operating_system.as_dict()
