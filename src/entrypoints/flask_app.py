from flask import Flask
from sqlalchemy.orm import sessionmaker

import settings
from src.adapters.data.models import db
from settings import Settings

session_factory = sessionmaker(bind=Settings.database_engine)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.Settings.database_url
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    create_app().run()
