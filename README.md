# kong-oauth2-workshop

## Setup upstream
Read `upstream/README.md` to setup the upstream
## Setup Kong

```sh
make gen-cert
make gen-cert-key
make build
make run_db
# wait for 30 seconds
make migrate
make run
```

## Test

```sh
curl http://localhost:8001/services
```

## Let the upstream be protected by OAuth2 plugin

### Add a service
```sh
curl --request POST \
  --url http://localhost:8001/services \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "stepcounts",
	"url": "http://host.docker.internal:5050/stepcounts"
}'
```

### Add a route
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

### Test route via Kong
> you will get `HTTP/1.1 401 UNAUTHORIZED`
```sh
curl -k --request GET \
  --url https://localhost:8000/stepon \
  --header 'Content-Type: application/json'
```

### Enable OAuth2 plugin for the route, and save the returned value `provision_key`
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

### Add a consumer
```sh
curl --request POST \
  --url http://localhost:8001/consumers \
  --header 'Content-Type: application/json' \
  --data '{
	"username": "shoeflyshoe"
}'
```

### Add OAuth2 credentials for the consumer, save the returned value `client_id` and `client_secret`
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

### Request Authorization Code, replace `client_id` and `provision_key` by what you got in previous steps. Save the returned value `code`
```sh
curl -k --request POST \
  --url https://localhost:8000/stepon/oauth2/authorize \
  --header 'Content-Type: application/json' \
  --data '{
	"client_id": "neEhJHdNlM08llc1W63OqP9jRGbabWvT",
	"response_type": "code",
	"scope": "step_counts",
	"provision_key": "V8OKoryTkT9RgrRRSaMe8RYnOvq5KIdZ",
	"authenticated_userid": "neil"
}'
```

### Exhange Authorization code for Access Token, replace `code`, `client_id` and `client_secret` by what you got in prevoius steps, save the retured value `access_token`
```sh
curl -k --request POST \
  --url https://localhost:8000/stepon/oauth2/token \
  --header 'Content-Type: application/json' \
  --data '{
	"grant_type": "authorization_code",
	"code": "NYhW6GIJGFwaBecPMYvTk1yJId8o30T3",
	"client_id": "neEhJHdNlM08llc1W63OqP9jRGbabWvT",
	"client_secret": "rW8pEccMF6Ni9zlv4bgei6mxrA4s3hSH"
}'
```

### Ruqest upstream again with `access_token`
```sh
curl -k --request GET \
  --url https://localhost:8000/stepon \
  --header 'Authorization: bearer 7pImqBHdT5eiIZIATrAVwHub9kSj5WL5' \
  --header 'Content-Type: application/json'
```


## Reference
- https://konghq.com/blog/kong-gateway-oauth2
- https://www.youtube.com/watch?v=AIYIHZbDziI&ab_channel=Kong
- https://docs.konghq.com/hub/kong-inc/oauth2/1.0.x.html