from sittingduck import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    steamid = db.Column(db.String(50), unique=False, nullable=False)
    userteam = db.Column(db.String(2), unique=False, nullable=False)
    mapname = db.Column(db.String(50), unique=False, nullable=False)
    mapround = db.Column(db.String(50), unique=False, nullable=False)
    posx = db.Column(db.Float, unique=False, nullable=False)
    posy = db.Column(db.Float, unique=False, nullable=False)
    posz = db.Column(db.Float, unique=False, nullable=False)
