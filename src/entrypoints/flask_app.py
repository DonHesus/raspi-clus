import os
import pathlib

import connexion
from sqlalchemy.orm import sessionmaker
from src.adapters.data.models import db
from settings import Settings


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
    create_app().run()
