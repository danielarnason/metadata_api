from flask import jsonify
from api import ma, meta_api
from flask_restful import Resource, reqparse
from api.models import Metadata
from api import db

class MetadataSchema(ma.ModelSchema):

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

    metadata_schema = MetadataSchema()

    def get(self, themename):
        table = Metadata.query.filter_by(themename=themename).first()
        return metadata_schema.jsonify(table)

    def delete(self, themename):
        table = Metadata.query.filter_by(themename=themename).first()
        db.session.delete(table)
        db.session.commit()

        return {'message': f'Metadata for {table.themename} slettet'}, 204
