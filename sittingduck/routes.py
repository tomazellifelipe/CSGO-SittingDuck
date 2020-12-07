import json

from flask import render_template, request, g
from sittingduck import app, db
from sittingduck.models import User


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
    g.user = 'Felipe'
    return g.user
