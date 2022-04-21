## A dummy upstream behind Kong proxy

### Setup
```sh
python3.9 -m venv venv
source ./venv/bin/activate
source ./venv/bin/activate
flask run --port 5050 --host 0.0.0.0
```

### Test

Simulate user is NOT logged on
```sh
curl --request GET \
  --url http://localhost:5050/stepcounts \
  --header 'Content-Type: application/json'
```

Simualte user is logged on.
```sh
curl --request GET \
  --url http://localhost:5050/stepcounts \
  --header 'Content-Type: application/json' \
  --header 'x-authenticated-userid: neil'
```

