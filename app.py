from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/danielarnason'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

class MetadataList(Resource):
    def get(self):
        metadata = Metadata.query.all()
        return [{'schema': i.schema, 'table': i.tablename} for i in metadata]

api.add_resource(MetadataList, '/metadata')


if __name__ == '__main__':
    app.run(debug=True)