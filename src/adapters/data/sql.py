from typing import List
from uuid import UUID

from src.domain.models import Cluster, RaspberryPi, OperatingSystem
from src.adapters.data.models import Cluster as DBCluster
from src.adapters.data.models import RaspberryPi as DBRaspberryPi
from src.adapters.data.models import OperatingSystem as DBOperatingSystem
from src.domain.ports import ClusterRepository, UnitOfWork, UnitOfWorkManager, RaspberryPiRepository, \
    OperatingSystemRepository


class SQLClusterRepository(ClusterRepository):
    __class__ = DBCluster

    def __init__(self, session):
        self._session = session

    def get_all(self):
        return DBCluster.query.all()

    def get_by_id(self, cluster_id: UUID):
        pass

    def add_cluster(self, cluster: Cluster):
        cluster_to_add = DBCluster(id=cluster.cluster_id, name=cluster.name, network=cluster.network)
        self._session.add(cluster_to_add)

    def update_cluster(self, cluster: Cluster):
        pass


class SQLRaspberryPiRepository(RaspberryPiRepository):

    def __init__(self, session):
        self._session = session

    def get_all(self) -> List[RaspberryPi]:
        return DBRaspberryPi.query.all()

    def add_raspberry_pi(self, raspberry: RaspberryPi):
        raspberry_to_add = DBRaspberryPi(id=raspberry.raspberry_id, name=raspberry.name, address=raspberry.address)
        self._session.add(raspberry_to_add)

    def get_by_id(self, raspberry_id: UUID) -> RaspberryPi:
        pass

    def update_raspberry(self, raspberry: RaspberryPi):
        pass


class SQLOperatingSystemRepository(OperatingSystemRepository):

    def __init__(self, session):
        self._session = session

    def get_all(self) -> List[OperatingSystem]:
        return DBOperatingSystem.query.all()

    def get_by_id(self, os_id: UUID) -> OperatingSystem:
        pass

    def add_operating_system(self, operating_system: OperatingSystem):
        os_to_add = DBOperatingSystem(operating_system.os_id, operating_system.name, operating_system.path)
        self._session.add(os_to_add)

    def update_operating_system(self, operating_system: OperatingSystem):
        pass


class SQLUnitOfWorkManager(UnitOfWorkManager):

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def start(self) -> UnitOfWork:
        return SQLUnitOfWork(session=self.session_factory())


class SQLUnitOfWork(UnitOfWork):

    def __init__(self, session):
        self._session = session

    def __enter__(self):
        return self

    def __exit__(self, ex_type, value, traceback):
        if value is None:
            self.commit()
        else:
            self.rollback()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()

    @property
    def clusters(self):
        return SQLClusterRepository(self._session)

    @property
    def raspberry_pis(self):
        return SQLRaspberryPiRepository(self._session)

    @property
    def operating_systems(self):
        return SQLOperatingSystemRepository(self._session)
