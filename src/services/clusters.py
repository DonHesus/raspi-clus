from src.domain.config_loader import ConfigLoader
from src.services import Handler


class GetAllClustersHandler(Handler):

    def handle(self):
        with self.manager.start() as uow:
            clusters = uow.clusters.get_all()

        return clusters

class AddClusterHandler(Handler):

    def handle(self, body):
        config_loader = ConfigLoader()
        objects = config_loader.translate_config(body)
        with self.manager.start() as uow:
            uow.clusters.add_cluster(objects)


class GetSingleClusterHandler(Handler):
    def handle(self, cluster_id = None, cluster_name = None):
        with self.manager as uow:
            if cluster_id:
                cluster = uow.cluster.get_by_id(cluster_id)
            elif cluster_name:
                cluster = uow.clusters.get_by_name(cluster_name)

        return cluster
