from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres@localhost:5432/danielarnason"
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
    """Resource for the whole Metadata table"""

    def get(self):
        metadata = Metadata.query.all()
        return metadata_schema.jsonify(metadata, many=True)

    def post(self):
        parser.add_argument("schema", type=str, required=True)
        parser.add_argument("tablename", type=str, required=True)
        parser.add_argument(
            "ansvarlig", type=str, required=False, default=None, store_missing=True
        )
        parser.add_argument(
            "center", type=str, required=False, default=None, store_missing=True
        )
        parser.add_argument(
            "email", type=str, required=False, default=None, store_missing=True
        )
        parser.add_argument(
            "beskrivelse", type=str, required=False, default=None, store_missing=True
        )
        args = parser.parse_args()

        ny_metadata = Metadata(
            schema=args["schema"],
            tablename=args["tablename"],
            ansvarlig=args["ansvarlig"],
            center=args["center"],
            email=args["email"],
            beskrivelse=args["beskrivelse"],
        )

        db.session.add(ny_metadata)
        db.session.commit()

        return {
            "message": f"Metadata om {ny_metadata.schema}.{ny_metadata.tablename} gemt i db"
        }

class MetadataItem(Resource):
    """Resource for items in the metadata table"""

    def delete(self, schema, tablename):
        table = Metadata.query.filter_by(schema=schema, tablename=tablename).first()
        db.session.delete(table)
        db.session.commit()

        return {'message': f'Metadata for {schema}.{tablename} slettet'}



api.add_resource(MetadataList, "/metadata")
api.add_resource(MetadataItem, '/metadata/<schema>.<tablename>')

if __name__ == "__main__":
    app.run(debug=True)
