from sqlalchemy.orm import sessionmaker

from adapters.data.sql import SQLUnitOfWorkManager
from services.health import RaspberryPiAliveHandler
from settings import Settings

session_factory = sessionmaker(bind=Settings.database_engine)

def health_status(raspberry_id):
    db_manager = SQLUnitOfWorkManager(session_factory)
    handler = RaspberryPiAliveHandler(db_manager)
    handler.handle(raspberry_id)
    return 204