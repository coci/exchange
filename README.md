### something to notice:
1- i used JWT as a authentication methods, so please consider some endpoints have permission. for more information please see Postman collections

2- i implemented this project based on user model which every order belongs to user

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
