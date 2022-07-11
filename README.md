# Imaging-beacon

## Setup

### Docker
#### Start the containers
```
docker-compose up -d
```
#### Remove containers and volumes
```
docker-compose down -v
```
### Running the api

#### Set env variables
```
export MONGODB_USERNAME=
export MONGODB_PASSWORD=
export MONGODB_HOSTNAME=
export MONGODB_DATABASE=
export FLASK_DEBUG=1 # set to zero if not needed
export FLASK_APP=./api/app.py
```
#### Start the mongodb container
```
docker-compose up -d mongodb
```
#### Install dependencies
```
pip install -r requirements.txt
```
#### Run api
```
flask run
```
