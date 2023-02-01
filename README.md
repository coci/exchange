### something to notice:
1- I used JWT as an authentication method, so please note that some endpoints have permission. For more information, please refer to the Postman collections.

2- I implemented this project based on the user model, where every order is associated with a user.

3- If you would like to call the endpoints and test the functionality, please follow the steps below. For API documentation, I chose to use the POSTMAN collection due to a lack of time to fully complete the task. (I could have used Swagger or OpenAPI for documentation instead.

4- i know there is possibilities that data might in Redis and Database might be lost and i have to persist their volume in docker, but in this task i didn't.

5- i think in real production, pending order must have expire time because there is possibilities that one order stay in pending forever, but in this task i didn't set expire time for pending order.
### to deploy:
```shell
docker-compose up -d
```

### to migrate database:
```shell
docker-compose exec exchange python3 manage.py migrate
```

### endpoints:
i add postman collection for api documentation :


<a id="raw-url" href="https://raw.githubusercontent.com/coci/exchange/master/exchange_postman.json" download="https://raw.githubusercontent.com/coci/exchange/master/exchange_postman.json">Download POSTMAN collection</a>

### to test project:
follow steps below :


1- call register user

2- get user token

3- add balance to user

4- make order


### run test cases:
```shell
docker-compose exec exchange python3 manage.py test
```
