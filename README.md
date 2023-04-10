# kong-oauth2-workshop

## 1) Setup upstream
### Setup and test uptream
> you will get a reponse with empty data
```sh
make run_upstream
curl http://localhost:5000/bio
```
## 2) Setup Kong and upstream

### Setup Kong
```sh
make gen-cert
make build_kong
make run_db
# wait for about 10 seconds
make migrate_kong
make run_kong
```

### Test Kong is ready
```sh
curl http://localhost:8001/services
```

### Add a service that can be public vist via Kong
```sh
curl --request POST \
  --url http://localhost:8001/services \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "bio_service",
	"url": "http://host.docker.internal:5000/bio"
}'
```

### Add a route
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

### Test route via Kong
> you can visit it but th resonse data is empty
```sh
curl -k --request GET \
  --url https://localhost:8000/bio \
  --header 'Content-Type: application/json'
```


## 3)Add OAuth2 plugin to protect the route
### Enable OAuth2 plugin for the route, and save the returned value of `provision_key`
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

### Test route via Kong
> you will get 401 Unauthorized
```sh
curl -k --request GET \
  --url https://localhost:8000/bio \
  --header 'Content-Type: application/json'
```

### Add a consumer
```sh
curl --request POST \
  --url http://localhost:8001/consumers \
  --header 'Content-Type: application/json' \
  --data '{
	"username": "user_a"
}'
```

### Add OAuth2 client for the consumer, save the returned value `client_id` and `client_secret`
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

### Request Authorization Code, replace `client_id` and `provision_key` by what you got in previous steps. Save the returned value `code`, you can replace `authenticated_userid` for any user you like.
```sh
curl -k --request POST \
  --url https://localhost:8000/user_service/oauth2/authorize \
  --header 'Content-Type: application/json' \
  --data '{
	"client_id": "REPLACE_ME",
	"response_type": "code",
	"scope": "biometric",
	"provision_key": "REPLACE_ME",
	"authenticated_userid": "neil"
}'
```

### Exhange Authorization code for Access Token, replace `code`, `client_id` and `client_secret` by what you got in prevoius steps, save the retured value `access_token`
```sh
curl -k --request POST \
  --url https://localhost:8000/user_service/oauth2/token \
  --header 'Content-Type: application/json' \
  --data '{
	"grant_type": "authorization_code",
	"code": "REPLACE_ME",
	"client_id": "REPLACE_ME",
	"client_secret": "REPLACE_ME"
}'
```

### Ruqest upstream without `access_token`
> you will get 401 and The access token is missing
```sh
curl -k --request GET \
  --url https://localhost:8000/user_service \
  --header 'Content-Type: application/json'
```

### Ruqest upstream with `access_token`
> Congrats! the route is protected by Access Token!
```sh
curl --request GET \
  --url https://localhost:8000/user_service \
  --header 'Authorization: bearer REPLACE_ME' \
  --header 'Content-Type: application/json'
```


## Reference
- https://konghq.com/blog/kong-gateway-oauth2
- https://www.youtube.com/watch?v=AIYIHZbDziI&ab_channel=Kong
- https://docs.konghq.com/hub/kong-inc/oauth2/1.0.x.html