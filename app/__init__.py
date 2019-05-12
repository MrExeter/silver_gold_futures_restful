import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()


def create_app(config_type):
    app = Flask(__name__)

    configuration = os.path.join(os.getcwd(), 'config', config_type + '.py')

    app.config.from_pyfile(configuration)

    db.init_app(app)  # bind database to flask app

    # Init ma
    ma = Marshmallow(app)

    class FutureSchema(ma.Schema):
        class Meta:
            fields = ('id', 'name', 'url')

    future_schema = FutureSchema(strict=True)
    futures_schema = FutureSchema(many=True, strict=True)

    return app
