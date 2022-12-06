from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.domain.models import Cluster, RaspberryPi, OperatingSystem


class ClusterRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, cluster_id: UUID):
        pass

    @abstractmethod
    def add_cluster(self, cluster: Cluster):
        pass

    @abstractmethod
    def update_cluster(self, cluster: Cluster):
        pass


class RaspberryPiRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[RaspberryPi]:
        pass

    @abstractmethod
    def get_by_id(self, raspberry_id: UUID) -> RaspberryPi:
        pass

    @abstractmethod
    def add_raspberry_pi(self, raspberry: RaspberryPi):
        pass

    @abstractmethod
    def update_raspberry(self, raspberry: RaspberryPi):
        pass


class OperatingSystemRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[OperatingSystem]:
        pass

    @abstractmethod
    def get_by_id(self, os_id: UUID) -> OperatingSystem:
        pass

    @abstractmethod
    def add_operating_system(self, operating_system: OperatingSystem):
        pass

    @abstractmethod
    def update_operating_system(self, operating_system: OperatingSystem):
        pass


class UnitOfWork(ABC):

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, type, value, traceback):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @property
    @abstractmethod
    def clusters(self):
        pass

    @property
    @abstractmethod
    def raspberry_pis(self):
        pass

    @property
    @abstractmethod
    def operating_systems(self):
        pass


class UnitOfWorkManager(ABC):

    @abstractmethod
    def start(self) -> UnitOfWork:
        pass
