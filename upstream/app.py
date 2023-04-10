from flask import Flask, request, abort
import json

app = Flask(__name__)

@app.route('/me')
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
        "foo": [
            { "date": "2021-01-01", "count": 14500 },
            { "date": "2021-01-02", "count": 6500 },
            { "date": "2021-01-03", "count": 28000 }
        ],
        "bar": [
            { "date": "2021-01-01", "count": 900 },
            { "date": "2021-01-02", "count": 1400 },
            { "date": "2021-01-03", "count": 1100 }
        ],
        "neil": [
            { "date": "2021-01-01", "count": 9100 },
            { "date": "2021-01-02", "count": 1100 },
            { "date": "2021-01-03", "count": 1300 }
        ]
    }

    return mock_data[u]


def get_user():
    user = request.headers.get('x-authenticated-userid')
    return user


if __name__ == "__main__":
    app.run(host="0.0.0.0")