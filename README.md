# kong-oauth2-workshop

## 1) Setup upstream
You will get a reponse with empty data.
```sh
make run_upstream
curl http://localhost:5000/bio
```
## 2) Setup Kong and upstream

### 2.1) Setup Kong
```sh
make gen-cert
make build_kong
make run_db
# wait for about 10 seconds
make migrate_kong
make run_kong
```

### 2.2) Test Kong is ready
```sh
curl http://localhost:8001/services
```

### 2.3) Add a service that can be public vist via Kong
```sh
curl --request POST \
  --url http://localhost:8001/services \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "bio_service",
	"url": "http://host.docker.internal:5000/bio"
}'
```

### 2.4) Add a route
```sh
curl --request POST \
  --url http://localhost:8001/routes \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "user_route",
	"service": {
		"name": "bio_service"
	},
	"paths": ["/bio"]
}'
```

### 2.5) Test route via Kong
> You can now visit the upstream via Kong!
```sh
curl -k --request GET \
  --url https://localhost:8000/bio \
  --header 'Content-Type: application/json'
```


## 3) Enable OAuth2
### 3.1) Enable OAuth2 plugin for the route.
> Save the returned value of `provision_key`
>
```sh
curl --request POST \
  --url http://localhost:8001/services/bio_service/plugins \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "oauth2",
	"config": {
		"scopes": [
			"user_profile",
			"email",
			"biometric"
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

### 3.2) Test route via Kong
> you will get 401 Unauthorized
```sh
curl -k --request GET \
  --url https://localhost:8000/bio \
  --header 'Content-Type: application/json'
```

### 3.3) Add a consumer
```sh
curl --request POST \
  --url http://localhost:8001/consumers \
  --header 'Content-Type: application/json' \
  --data '{
	"username": "user_a"
}'
```

### 3.4) Add OAuth2 client for the consumer
> save the returned value of `client_id` and `client_secret`
```sh
curl --request POST \
  --url http://localhost:8001/consumers/user_a/oauth2 \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "Kong workshop user",
	"redirect_uris": [
		"https://fakeurl"
	]
}'
```

### 3.5) Request Authorization Code,
> replace `client_id` and `provision_key` by what you got in previous steps.
> Save the returned value `code`.

```sh
curl -k --request POST \
  --url https://localhost:8000/bio_service/oauth2/authorize \
  --header 'Content-Type: application/json' \
  --data '{
	"client_id": "REPLACE_ME",
	"response_type": "code",
	"scope": "biometric",
	"provision_key": "REPLACE_ME",
	"authenticated_userid": "neil"
}'
```

### 3.6) Exhange Authorization code for Access Token,
> replace `code`, `client_id` and `client_secret` by what you got in prevoius steps,
> save the retured value `access_token`

```sh
curl -k --request POST \
  --url https://localhost:8000/bio_service/oauth2/token \
  --header 'Content-Type: application/json' \
  --data '{
	"grant_type": "authorization_code",
	"code": "REPLACE_ME",
	"client_id": "REPLACE_ME",
	"client_secret": "REPLACE_ME"
}'
```

### 3.7) Ruqest upstream without `access_token`
> you will get 401 and The access token is missing
```sh
curl -k --request GET \
  --url https://localhost:8000/bio_service \
  --header 'Content-Type: application/json'
```

### 3.8) Ruqest upstream with `access_token`
> Congrats! the route is protected by Access Token!
```sh
curl -k --request GET \
  --url https://localhost:8000/bio \
  --header 'Authorization: bearer REPLACE_ME' \
  --header 'Content-Type: application/json'
```


## Reference
- https://konghq.com/blog/kong-gateway-oauth2
- https://www.youtube.com/watch?v=AIYIHZbDziI&ab_channel=Kong
- https://docs.konghq.com/hub/kong-inc/oauth2/1.0.x.html