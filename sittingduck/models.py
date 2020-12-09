from datetime import datetime

from sittingduck import db


class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(db.String(50), unique=True, nullable=False)
    origem_x = db.Column(db.Float, nullable=False)
    origem_y = db.Column(db.Float, nullable=False)
    scale = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f"Map({self.mapName}, {self.mapOrigem_x}, {self.mapOrigem_y})"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    steamid = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    matches = db.relationship('Match', backref='player', lazy=True)

    def __repr__(self) -> str:
        return f"User({self.username}, {self.steamid})"


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.utcnow)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rounds = db.relationship('Round', backref='match', lazy=True)

    def __repr__(self) -> str:
        return f"Match({self.mapName}, {self.matchDate})"


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currentRound = db.Column(db.Integer, nullable=False)
    ctScore = db.Column(db.Integer, nullable=False)
    tScore = db.Column(db.Integer, nullable=False)
    matchId = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    status = db.relationship('Status', backref='round', lazy=True)

    def __repr__(self) -> str:
        return f"Round({self.currentRound}, {self.ctScore}, {self.tScore})"


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    health = db.Column(db.Integer, nullable=False)
    positionX = db.Column(db.Integer, nullable=False)
    positionY = db.Column(db.Integer, nullable=False)
    positionZ = db.Column(db.Integer, nullable=False)
    weaponInHand = db.Column(db.String(50), nullable=False)
    roundId = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Status({self.health}, {self.weaponInHand})"
