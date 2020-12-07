import io
import json
from PIL import Image

from flask import Response, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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
            mapname = csgopayload['map']['name'].split('/')[-1]
            user = User(username=csgopayload['player']['name'],
                        steamid=csgopayload['player']['steamid'],
                        userteam=csgopayload['player']['team'],
                        mapname=mapname,
                        mapround=csgopayload['map']['round'],
                        posx=positions[0],
                        posy=positions[1],
                        posz=positions[2])
            db.session.add(user)
            db.session.commit()
    return (json.dumps({'success': True}),
            200,
            {'ContentType': 'application/json'})


@app.route('/debug')
def debug():
    plotdata()
    return 'debugmode'


@app.route('/plot.png')
def plot_png():
    fig = plotdata()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def plotdata():
    img = Image.open('sittingduck\\images\\de_overpass.jpg')
    data = User.query.all()
    pos_x = [row.posx for row in data if row.mapround == '0']
    pos_y = [row.posy for row in data if row.mapround == '0']
    fig = Figure(figsize=(2**5, 2**5))
    ax = fig.add_subplot()
    ax.plot(pos_x, pos_y, 'ro')
    ax.imshow(img, extent=(-4831, 494, -3544, 1781))
    ax.axis([-4831, 494, -3544, 1781])
    ax.axis('off')
    return fig
