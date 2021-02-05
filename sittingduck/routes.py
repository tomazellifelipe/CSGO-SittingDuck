import io
import json
from PIL import Image

from flask import Response, render_template, request, flash, redirect
from flask.helpers import url_for
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt

from sittingduck import app, db
from sittingduck.models import Round, Status, Match
from sittingduck.forms import RegistrationForm, LoginForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'admin':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessfull. Please check steamid and password',
                  'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/cslog')
def csgo():
    return render_template('userinfo.html')


@app.route('/api/csgo', methods=['POST'])
def csgoapi():
    csgopayload = request.get_json()
    if csgopayload['player']['activity'] == 'playing':
        if csgopayload['round']['phase'] == 'live':
            match = Match.query.get(1)  # hardcoded
            logRound(csgopayload=csgopayload, match=match)
    return (json.dumps({'success': True}),
            200,
            {'ContentType': 'application/json'})


@app.route('/debug')
def debug():
    plotdata()
    return 'debugmode'


@app.route('/plot.png')
def plot_png():
    fig = plotdata(15)  # hardcoded
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def plotdata(num):
    img = Image.open('sittingduck\\images\\de_overpass.dds')  # hardcoded
    round = Round.query.filter_by(currentRound=num).first()
    if round:
        status = Status.query.filter_by(roundId=round.id).all()
        statusHealth = Status.query.filter_by(health=0,
                                              roundId=round.id).first()
        pos_x = [row.positionX for row in status]
        pos_y = [row.positionY for row in status]
        fig, ax = plt.subplots()
        ax.plot(pos_x, pos_y, 'r')
        if statusHealth:
            ax.plot(statusHealth.positionX, statusHealth.positionY, 'bx')
        ax.imshow(img, extent=(-4831, 494, -3544, 1781))  # hardcoded
        ax.axis([-4831, 494, -3544, 1781])  # hardcoded
        ax.axis('off')
        return fig


def logRound(csgopayload, match):
    currentRound = Round.query.filter_by(
        currentRound=csgopayload['map']['round'], matchId=match.id).first()
    if currentRound:
        logStatus(csgopayload=csgopayload, currentRound=currentRound)
    else:
        round = Round(currentRound=csgopayload['map']['round'],
                      ctScore=csgopayload['map']['team_ct']['score'],
                      tScore=csgopayload['map']['team_t']['score'],
                      matchId=match.id)
        db.session.add(round)
        db.session.commit()
        currentRound = Round.query.filter_by(
            currentRound=csgopayload['map']['round'], matchId=match.id).first()
        logStatus(csgopayload=csgopayload, currentRound=currentRound)


def logStatus(csgopayload, currentRound):
    positions = [float(pos.strip()) for pos in
                 csgopayload['player']['position'].split(',')]
    weaponInHand = ""
    for key in csgopayload['player']['weapons']:
        if csgopayload['player']['weapons'][key]['state'] == "active":
            weaponInHand = csgopayload['player']['weapons'][key]['name']
    status = Status(health=csgopayload['player']['state']['health'],
                    positionX=positions[0],
                    positionY=positions[1],
                    positionZ=positions[2],
                    weaponInHand=weaponInHand,
                    roundId=currentRound.id)
    db.session.add(status)
    db.session.commit()
