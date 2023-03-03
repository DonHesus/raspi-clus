import logging
import pathlib
import connexion
from sqlalchemy.orm import sessionmaker
from src.adapters.data.models import db

from settings import Settings

logger = logging.getLogger("raspi_clus_server")
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(Settings.logging_file)
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

session_factory = sessionmaker(bind=Settings.database_engine)


def create_app():
    openapi_dir = f"{pathlib.Path(__file__).parent.parent}/adapters/rest_api"
    connexion_app = connexion.FlaskApp(__name__, port=5000, specification_dir=openapi_dir)
    connexion_app.add_api("openapi.yaml")
    app = connexion_app.app
    app.config['SQLALCHEMY_DATABASE_URI'] = Settings.database_url
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    logger.info("Raspi clus starting")
    create_app().run("0.0.0.0")
