# imaging-beacon
`imaging-beacon` is a metadata discovery service inspired by [GA4GH Beacon](https://beacon-project.io/) used for finding imaging data.

## Configuration
The following environment variables can be given in a `.env` file for `docker-compose`.
```
APP_HOST=localhost
APP_PORT=8080
APP_CORS=False
APP_INFO=api/config/info.json
DB_HOST=localhost
DB_PORT=27017
DB_NAME=beacon
DB_AUTH=admin
DB_USERNAME=username
DB_PASSWORD=password
```
The environment variables can be loaded for development with:
```
export $(grep -v '^#' .env | xargs)
```

## Development
Running the application for development
```
python -m api.app
```

Checking code style, linting and typing
```
tox -p auto
```

## Deployment
Building an image with `docker` and deploying the database and application with `docker-compose`.
```
docker-compose up -d
```
