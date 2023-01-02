from sqlalchemy.orm import sessionmaker

from settings import Settings
from src.adapters.data.sql import SQLUnitOfWorkManager
from src.services.clusters import GetAllClustersHandler, AddClusterHandler, GetSingleClusterHandler

session_factory = sessionmaker(bind=Settings.database_engine)

def get_clusters():
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = GetAllClustersHandler(db_manager)
    clusters = handler.handle()
    return clusters, 200

def add_cluster(body: dict):
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = AddClusterHandler(uow_manager=db_manager)
    handler.handle(body)
    return "Success", 201

def get_cluster(id: int):
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = GetSingleClusterHandler(db_manager)
    cluster = handler.handle(id)
    return cluster, 200
