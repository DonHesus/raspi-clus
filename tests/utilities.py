from typing import List
from uuid import UUID

from domain.models import RaspberryPi
from domain.ports import UnitOfWorkManager, UnitOfWork, ClusterRepository, RaspberryPiRepository


class MockManager(UnitOfWorkManager):

    def start(self) -> UnitOfWork:
        return MockUOW()


class MockUOW(UnitOfWork):
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    @property
    def clusters(self) -> ClusterRepository:
        pass

    @property
    def raspberry_pis(self):
        return MockRepository()

    @property
    def operating_systems(self):
        pass

class MockRepository(RaspberryPiRepository):
    def get_all(self) -> List[RaspberryPi]:
        pass

    def get_by_id(self, raspberry_id: UUID) -> RaspberryPi:
        pass

    def add_raspberry_pi(self, raspberry: RaspberryPi):
        pass

    def update_raspberry(self, raspberry: RaspberryPi):
        pass