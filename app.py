from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)


class Metadata(db.Model):
    """Model i databasen"""

    id = db.Column(db.Integer, primary_key=True)
    themename = db.Column(db.String(100), unique=False, nullable=True)
    center = db.Column(db.String(3), unique=False, nullable=True)
    afdeling = db.Column(db.String(100), unique=False, nullable=True)
    email = db.Column(db.String(100), unique=False, nullable=True)
    telefonnr = db.Column(db.String(8), unique=False, nullable=True)
    ansvarlig = db.Column(db.String(100), unique=False, nullable=True)
    beskrivelse = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Metadata({self.id}, {self.themename})"


class MetadataSchema(ma.ModelSchema):
    """Schema for Marshmallow"""

    class Meta:
        model = Metadata


metadata_schema = MetadataSchema()
parser = reqparse.RequestParser()


class MetadataList(Resource):
    """Resource for the whole Metadata table"""

    def get(self):
        metadata = Metadata.query.all()
        return metadata_schema.jsonify(metadata, many=True)

    def post(self):
        parser.add_argument("themename", type=str, required=True)
        parser.add_argument(
            "ansvarlig", type=str, required=False, default=None, store_missing=True
        )
        parser.add_argument(
            "center", type=str, required=False, default=None, store_missing=True
        )
        parser.add_argument(
            "afdeling", type=str, required=False, default=None, store_missing=True
        )
        parser.add_argument(
            "email", type=str, required=False, default=None, store_missing=True
        )
        parser.add_argument(
            "telefonnr", type=str, required=False, default=None, store_missing=True
        )
        parser.add_argument(
            "beskrivelse", type=str, required=False, default=None, store_missing=True
        )
        args = parser.parse_args()

        if len(Metadata.query.filter_by(themename=args['themename']).all()) > 0:
            return {'message': f'Metadata om {args["themename"]} eksisterer i forvejen'}, 422

        ny_metadata = Metadata(
            themename=args["themename"],
            ansvarlig=args["ansvarlig"],
            center=args["center"],
            afdeling=args["afdeling"],
            telefonnr=args["telefonnr"],
            email=args["email"],
            beskrivelse=args["beskrivelse"],
        )

        db.session.add(ny_metadata)
        db.session.commit()

        return {
            "message": f"Metadata om {ny_metadata.themename} gemt i db"
        }, 201

class MetadataItem(Resource):
    """Resource for items in the metadata table"""

    def get(self, themename):
        table = Metadata.query.filter_by(themename=themename).first()
        return metadata_schema.jsonify(table)

    def delete(self, themename):
        table = Metadata.query.filter_by(themename=themename).first()
        db.session.delete(table)
        db.session.commit()

        return {'message': f'Metadata for {table.themename} slettet'}, 204



api.add_resource(MetadataList, "/metadata")
api.add_resource(MetadataItem, '/metadata/<themename>')

if __name__ == "__main__":
    app.run(debug=True)
