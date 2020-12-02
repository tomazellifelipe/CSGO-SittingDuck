import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template, request

from player import Map, Player

app = Flask(__name__)
userinfo = [0]
userdata = dict()
positionaldata = {'pos_x': [], 'pos_y': [], 'pos_z': []}


def plotPosition(userdata):
    position = userdata['position']
    for pos in position:
        x, y, z = pos.split(",")
        positionaldata['pos_x'].append(float(x.strip()))
        positionaldata['pos_y'].append(float(y.strip()))
        positionaldata['pos_z'].append(float(z.strip()))
    df = pd.DataFrame(positionaldata)
    plt.plot(df['pos_x'], df['pos_y'], 'ro')
    plt.axis([-4831,  494, -3542, 1781])
    plt.show()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/cslog')
def csgo():
    return render_template('userinfo.html', userinfo=userdata)


@app.route('/api/csgo', methods=['POST'])
def csgoapi():
    data = request.get_json()
    _player = Player(data['player']['steamid'], data['player']['name'])
    if data['player']['activity'] == 'playing':
        _map = Map(data['map']['mode'], data['map']['name'])
        _map.phase = data['map']['phase']
        if _map.phase == 'live':
            _player.position.append(
                data['allplayers'][_player.steamid]['position'])
    userdata.update(_player.__dict__)
    print(userdata)
    return 'ok'


@app.route('/debug')
def debug():
    plotPosition(userdata)
    return render_template('debug.html')


if __name__ == '__main__':
    app.run(debug=True)
