from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost:5432/danielarnason"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Metadata(db.Model):
    """Model i databasen"""

    id = db.Column(db.Integer, primary_key=True)
    schema = db.Column(db.String(100), unique=False, nullable=False)
    tablename = db.Column(db.String(100), unique=False, nullable=False)
    center = db.Column(db.String(3), unique=False, nullable=True)
    email = db.Column(db.String(100), unique=False, nullable=True)
    ansvarlig = db.Column(db.String(100), unique=False, nullable=True)
    beskrivelse = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Metadata({self.id}, {self.schema}, {self.tablename})"


class MetadataSchema(ma.ModelSchema):
    """Schema for Marshmallow"""

    class Meta:
        model = Metadata


metadata_schema = MetadataSchema()
parser = reqparse.RequestParser()


class MetadataList(Resource):
    """Resource for restful api"""

    def get(self):
        metadata = Metadata.query.all()
        return metadata_schema.jsonify(metadata, many=True)

    def post(self):
        parser.add_argument('schema', type=str, required=True)
        parser.add_argument('tablename', type=str, required=True)
        args = parser.parse_args()

        ny_data = Metadata(schema=args['schema'], tablename=args['tablename'])
        db.session.add(ny_data)
        db.session.commit()

        return {
            'status': True,
            'message': 'Ny tabel gemt i db'
        }, 200
        


api.add_resource(MetadataList, "/metadata")

if __name__ == "__main__":
    app.run(debug=True)
