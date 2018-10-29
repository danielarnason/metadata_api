from app import db

class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schema = db.Column(db.String(100), unique=False, nullable=False)
    tablename = db.Column(db.String(100), unique=False, nullable=False)
    center = db.Column(db.String(3), unique=False, nullable=True)
    email = db.Column(db.String(100), unique=False, nullable=True)
    ansvarlig = db.Column(db.String(100), unique=False, nullable=True)
    beskrivelse = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'Metadata({self.id}, {self.schema}, {self.tablename})'