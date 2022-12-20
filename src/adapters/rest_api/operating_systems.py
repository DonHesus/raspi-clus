from sqlalchemy.orm import sessionmaker

from settings import Settings
from src.adapters.data.sql import SQLUnitOfWorkManager
from src.services.operating_systems import GetAllOperatingSystems, GetSingleOperatingSystemHandler, AddOperatingSystemHandler

session_factory = sessionmaker(bind=Settings.database_engine)

def get_operating_systems():
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = GetAllOperatingSystems(db_manager)
    oses = handler.handle()
    return oses, 200

def get_single_os(os_id):
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = GetSingleOperatingSystemHandler(db_manager)
    operating_system = handler.handle(os_id)
    return operating_system, 200

def add_operating_system(body):
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = AddOperatingSystemHandler(db_manager)
    handler.handle(body)
    return "Success", 201