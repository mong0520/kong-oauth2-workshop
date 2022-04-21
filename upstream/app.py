from flask import Flask, request, abort
import json

app = Flask(__name__)

@app.route('/stepcounts')
def stepcounts():

    authed_user = get_user()
    if not authed_user:
        return abort(401)
    msg = dict()
    msg['username'] = authed_user
    msg['data'] = get_data(authed_user)

    return msg


def get_data(u):
    mock_data = {
        "alice": [
            { "date": "2021-01-01", "count": 14500 },
            { "date": "2021-01-02", "count": 6500 },
            { "date": "2021-01-03", "count": 28000 }
        ],
        "bob": [
            { "date": "2021-01-01", "count": 900 },
            { "date": "2021-01-02", "count": 1400 },
            { "date": "2021-01-03", "count": 1100 }
        ],
        "neil": [
            { "date": "2021-01-01", "count": 2500 },
            { "date": "2021-01-02", "count": 12000 },
            { "date": "2021-01-03", "count": 9500 }
        ]
    }

    return mock_data[u]


def get_user():
    user = request.headers.get('x-authenticated-userid')
    return user


if __name__ == "__main__":
    app.run(host="0.0.0.0")