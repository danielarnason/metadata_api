from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
import os

meta_api = Api()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.realpath('app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from api.resources import MetadataList, MetadataItem
    meta_api.add_resource(MetadataList, "/metadata")
    meta_api.add_resource(MetadataItem, '/metadata/<themename>')

    meta_api.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    return app