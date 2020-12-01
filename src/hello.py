from flask import Flask, request, render_template
from player import Player

app = Flask(__name__)
userinfo = dict()
player = Player('76561198263058338')


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/cslog')
def csgo():
    return render_template('userinfo.html', userinfo=userinfo)


@app.route('/api/csgo', methods=['POST'])
def csgoapi():
    positionsJson = request.get_json()
    player.position.append(
        positionsJson['allplayers'][player.steamid]['position'])
    userinfo.update(positionsJson)
    return 'This is a POST route for CS:GO Game Integration'


@app.route('/debug')
def debug():
    print(player.position)
    return 'Ok'


if __name__ == '__main__':
    app.run(debug=True)
