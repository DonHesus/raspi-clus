from settings import Settings
from src.adapters.data.sql import SQLUnitOfWorkManager
from src.services.raspberry_pis import GetAllRaspberries, AddRaspberryPiHandler, GetSingleRaspberryPiHandler, \
    ChangeOSHandler, RefreshOSHandler
from src.adapters.data import sessionmaker

session_factory = sessionmaker(bind=Settings.database_engine)


def get_raspberries():
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = GetAllRaspberries(db_manager)
    raspberries = handler.handle()
    return raspberries, 200


def get_single_raspberry(mac_address: str):
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = GetSingleRaspberryPiHandler(db_manager)
    raspberry = handler.handle(mac_address)
    return raspberry, 200


def add_raspberry_pi(body: dict):
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = AddRaspberryPiHandler(db_manager)
    handler.handle(body)
    return "Success", 201


def change_os(mac_address, body: dict):
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = ChangeOSHandler(db_manager)
    handler.handle(mac_address=mac_address, os_id=body["os_id"])
    return 204


def refresh_os(mac_address):
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = RefreshOSHandler(db_manager)
    handler.handle(mac_address)
    return 204
