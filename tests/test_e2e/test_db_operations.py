import ipaddress
import uuid

import pytest

from settings import Settings
from src.adapters.data.sql import SQLUnitOfWorkManager
from src.domain.models import Cluster
from sqlalchemy.orm import sessionmaker

from src.entrypoints.flask_app import create_app

session_factory = sessionmaker(bind=Settings.database_engine)


@pytest.fixture
def app():
    app = create_app()
    yield app


class TestDBOperations:

    # def __init__(self):
    #     create_app().run()

    def test_get_all_cluster(self, app):
        with app.app_context():
            test_cluster = Cluster(cluster_id=uuid.uuid4(), name="Test_cluster",
                                   network=str(ipaddress.IPv4Network("192.164.50.11")))
            db_manager = SQLUnitOfWorkManager(session_factory=session_factory)
            with db_manager.start() as manager:
                manager.clusters.add_cluster(test_cluster)

            with db_manager.start() as manager:
                db_clusters = manager.clusters.get_all()

            assert test_cluster.cluster_id in [a.id for a in db_clusters]

    def test_get_all_raspberry_pi(self):
        pass

    def test_get_all_oses(self):
        pass

    def test_accessing_objects(self):
        pass
