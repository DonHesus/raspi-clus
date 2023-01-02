import uuid

from domain.models import Cluster
from src.services import Handler


class GetAllClustersHandler(Handler):

    def handle(self):
        with self.manager.start() as uow:
            clusters = uow.clusters.get_all()
            clusters_list = [cluster.as_dict() for cluster in clusters]

        return clusters_list

class AddClusterHandler(Handler):

    def handle(self, body: dict):
        body["cluster_id"] = uuid.uuid4()
        with self.manager.start() as uow:
            uow.clusters.add_cluster(Cluster(**body))


class GetSingleClusterHandler(Handler):
    def handle(self, id = None, cluster_name = None):
        with self.manager.start() as uow:
            if id:
                cluster = uow.clusters.get_by_id(id)
            elif cluster_name:
                cluster = uow.clusters.get_by_name(cluster_name)

        return cluster.as_dict()
