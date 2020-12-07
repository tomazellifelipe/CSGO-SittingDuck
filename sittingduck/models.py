from datetime import datetime
from enum import unique

from sqlalchemy.orm import backref
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


class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mapName = db.Column(db.String(50), unique=True, nullable=False)
    mapImage = db.Column(db.String(50), unique=True, nullable=False)
    mapOrigem_x = db.Column(db.Float, nullable=False)
    mapOrigem_y = db.Column(db.Float, nullable=False)
    mapScale = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f"Map({self.mapName}, {self.mapOrigem_x}, {self.mapOrigem_y}, {self.mapScale})"


class User2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    steamid = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    matches = db.relationship('Match', backref='player', lazy=True)

    def __repr__(self) -> str:
        return f"User({self.username}, {self.steamid})"


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mapName = db.Column(db.String(50), nullable=False)
    matchDate = db.Column(db.DateTime, nulllable=False,
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
        return f'Round({self.currentRound}, {self.ctScore}, {self.tScore})'


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playerHealth = db.Column(db.Integer, nullable=False)
    playerPositionX = db.Column(db.Integer, nullable=False)
    playerPositionY = db.Column(db.Integer, nullable=False)
    playerPositionZ = db.Column(db.Integer, nullable=False)
    playerWeaponInHand = db.Column(db.String(50), nullable=False)
    roundId = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)

    def __repr__(self) -> str:
        return f'Status({self.playerHealth}, {self.playerWeaponInHand})'
