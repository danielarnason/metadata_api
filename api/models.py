from api import db

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