from flask import Flask, request, render_template

app = Flask(__name__)
userinfo = dict()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/cslog')
def csgo():
    return render_template('userinfo.html', userinfo=userinfo)


@app.route('/api/csgo', methods=['POST'])
def csgoapi():
    userinfo.update(request.get_json())
    return 'This is a POST route for CS:GO Game Integration'


if __name__ == '__main__':
    app.run(debug=True)
