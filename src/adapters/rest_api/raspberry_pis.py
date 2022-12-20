from sqlalchemy.orm import sessionmaker

from settings import Settings
from src.adapters.data.sql import SQLUnitOfWorkManager
from src.services.raspberry_pis import GetAllRaspberries, AddRaspberryPiHandler, GetSingleRaspberryPiHandler

session_factory = sessionmaker(bind=Settings.database_engine)

def get_raspberries():
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = GetAllRaspberries(db_manager)
    raspberries = handler.handle()
    return raspberries, 200

def get_single_raspberry(raspberry_id):
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = GetSingleRaspberryPiHandler(db_manager)
    raspberry = handler.handle(raspberry_id)
    return raspberry, 200

def add_raspberry_pi(body: dict):
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = AddRaspberryPiHandler(db_manager)
    handler.handle(body)
    return "Success", 201

def change_os(os_id):
    raise NotImplementedError