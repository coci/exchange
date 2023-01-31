### something to notice:
1- i used JWT as a authentication methods, so please consider some endpoints have permission. for more information please see Postman collections

2- i implemented this project based on user model which every order belongs to user

3- if you mind to call endpoints and test functionality please just consider go through steps below and for api documentation i choose POSTMAN collection because of lack of time to accomplish all aspects of task ( i could use Swagger or OpenAPi for documentation )

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
