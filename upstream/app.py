from flask import Flask, request, abort
import json

app = Flask(__name__)

@app.route('/bio')
def stepcounts():

    authed_user = get_user()
    msg = {'username': None, 'data': None}
    if not authed_user:
        return msg
    msg['username'] = authed_user
    msg['data'] = get_data(authed_user)
    return msg


def get_data(u):
    mock_data = {
        "neil": { "birthday": "1984-05-20", "gender": 'male' },
        "john": { "birthday": "1984-01-01", "gender": 'male' },
        "may": { "birthday": "1984-08-13", "gender": 'female' },
    }

    return mock_data[u]


def get_user():
    user = request.headers.get('x-authenticated-userid')
    return user


if __name__ == "__main__":
    app.run(host="0.0.0.0")