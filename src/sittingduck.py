import json

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sittingduck.db'
db = SQLAlchemy(app)


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


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/cslog')
def csgo():
    return render_template('userinfo.html')


@app.route('/api/csgo', methods=['POST'])
def csgoapi():
    csgopayload = request.get_json()
    if csgopayload['player']['activity'] == 'playing':
        db.create_all()
        if csgopayload['round']['phase'] == 'live' and \
           csgopayload['player']['state']['health'] != 0:
            positions = [float(pos.strip()) for pos in
                         csgopayload['player']['position'].split(',')]
            user = User(username=csgopayload['player']['name'],
                        steamid=csgopayload['player']['steamid'],
                        userteam=csgopayload['player']['team'],
                        mapname=csgopayload['map']['name'],
                        mapround=csgopayload['map']['round'],
                        posx=positions[0],
                        posy=positions[1],
                        posz=positions[2])
            db.session.add(user)
            db.session.commit()
    else:
        db.drop_all()
    return (json.dumps({'success': True}),
            200,
            {'ContentType': 'application/json'})


@app.route('/debug')
def debug():
    print(User.query.all())
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True, port=5050)
