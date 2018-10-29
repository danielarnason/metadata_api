from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)

api = Api(app)

metadata = {
    'hello': 'WORLD!!!'
}

class MetadataList(Resource):
    def get(self):
        return metadata

api.add_resource(MetadataList, '/metadata')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/danielarnason'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)