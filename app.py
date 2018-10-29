from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/danielarnason'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)


db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import *

class MetadataSchema(ma.Schema):
    class Meta:
        fields = ["schema", "tablename"]

metadata_schema = MetadataSchema()

class MetadataList(Resource):
    def get(self):
        metadata = Metadata.query.all()
        return metadata_schema.jsonify(metadata, many=True)

api.add_resource(MetadataList, '/metadata')


if __name__ == '__main__':
    app.run(debug=True)