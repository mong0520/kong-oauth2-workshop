# kong-oauth2-workshop

## Setup

```sh
make gen-cert
make gen-cert-key
make bulid
make run_db
make migrate
make run
```

## Test

```sh
http://localhost:8001/services
```

## Let the upstream be protected by OAuth2 plugin

- Add a service
> replace ip address by what your flask app listens on.
```sh
curl --request POST \
  --url http://localhost:8001/services \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "stepcounts",
	"url": "http://10.58.0.77:5050/stepcounts"
}'
```

- Add a route
```sh
curl --request POST \
  --url http://localhost:8001/routes \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "stepon",
	"service": {
		"name": "stepcounts"
	},
	"paths": ["/stepon"]
}'
```

- Test route via Kong
```sh
curl --request GET \
  --url https://localhost:8000/stepon \
  --header 'Content-Type: application/json'
```

- Enable OAuth2 plugin for the route, and save the returned value `provision_key`
```sh
curl --request POST \
  --url http://localhost:8001/services/stepcounts/plugins \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "oauth2",
	"config": {
		"scopes": [
			"user_profile",
			"email",
			"biometric",
			"step_counts"
		],
		"mandatory_scope": true,
		"enable_authorization_code": true
	},
	"protocols": [
		"http",
		"https"
	]
}'
```

- Add a consumer
```sh
curl --request POST \
  --url http://localhost:8001/consumers \
  --header 'Content-Type: application/json' \
  --data '{
	"username": "shoeflyshoe"
}'
```

- Add OAuth2 credentials for the consumer, save the returned value `client_id` and `client_secret`
```sh
curl --request POST \
  --url http://localhost:8001/consumers/shoeflyshoe/oauth2 \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "Shoe Fly Shoe Customer Rewards",
	"redirect_uris": [
		"https://fakeurl"
	]
}'
```

- Request Authorization Code, replace `client_id` and `provision_key` by what you got in previous steps. Save the returned value `code`
```sh
curl --request POST \
  --url https://localhost:8000/stepon/oauth2/authorize \
  --header 'Content-Type: application/json' \
  --data '{
	"client_id": "lmsif4IbZeyQh2DmlxLE6l9rmaYKQTAE",
	"response_type": "code",
	"scope": "step_counts",
	"provision_key": "unKTv1nJ50T9gn6oo6OWhB7YM4ooUfj3",
	"authenticated_userid": "neil"
}'
```

- Exhange Authorization code for Access Token, replace `code`, `client_id` and `client_secret` by what you got in prevoius steps, save the retured value `access_token`
```sh
curl --request POST \
  --url https://localhost:8000/stepon/oauth2/token \
  --header 'Content-Type: application/json' \
  --data '{
	"grant_type": "authorization_code",
	"code": "0WWTnj5gUfpwzMeBMSlh9Rj8t4Izk6Hz",
	"client_id": "lmsif4IbZeyQh2DmlxLE6l9rmaYKQTAE",
	"client_secret": "mqfJWzreNvnjIFJLamPJIx0Mv1pVVZX8"
}'
```

- Ruqest upstream again with `access_token`
```sh
curl --request GET \
  --url https://localhost:8000/stepon \
  --header 'Authorization: bearer ciSL5IufVjurhJFiwosR6xuQWtJ1BQhl' \
  --header 'Content-Type: application/json'
```