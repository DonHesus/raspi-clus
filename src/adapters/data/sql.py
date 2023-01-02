import datetime
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
        cluster = DBCluster.query.get({"id" : cluster_id})
        return cluster

    def get_by_name(self, cluster_name):
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
        raspberry_to_add = DBRaspberryPi(id=raspberry.raspberry_id, name=raspberry.name, address=raspberry.address,
                                         cluster_id = raspberry.cluster_id)
        self._session.add(raspberry_to_add)

    def get_by_id(self, raspberry_id: UUID) -> RaspberryPi:
        return self._session.query(DBRaspberryPi).get({"id": raspberry_id})

    def update_raspberry(self, raspberry: RaspberryPi):
        pass

    def update_raspberry_system(self, raspberry_id, os_id):
        raspberry_obj = self._session.query(DBRaspberryPi).get({"id": raspberry_id})
        raspberry_obj.operating_system_id = os_id

    def update_last_alive(self, raspberry_id, date):
        raspberry_obj = self._session.query(DBRaspberryPi).get({"id": raspberry_id})
        raspberry_obj.last_alive = date


class SQLOperatingSystemRepository(OperatingSystemRepository):

    def __init__(self, session):
        self._session = session

    def get_all(self) -> List[OperatingSystem]:
        return DBOperatingSystem.query.all()

    def get_by_id(self, os_id: UUID) -> OperatingSystem:
        return DBOperatingSystem.query.get({"id": os_id})

    def add_operating_system(self, operating_system: OperatingSystem):
        os_to_add = DBOperatingSystem(id = operating_system.os_id, name=operating_system.name, path=operating_system.path)
        self._session.add(os_to_add)

    def update_operating_system(self, operating_system: OperatingSystem):
        pass


class SQLUnitOfWorkManager(UnitOfWorkManager):

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def start(self) -> UnitOfWork:
        return SQLUnitOfWork(session=self.session_factory)


class SQLUnitOfWork(UnitOfWork):

    def __init__(self, session):
        self._session = session

    def __enter__(self):
        self._session = self._session()
        return self

    def __exit__(self, ex_type, value, traceback):
        if value is None:
            self.commit()
        else:
            self.rollback()

    def commit(self):
        self._session.commit()
        self._session.close()

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
