# Image recognition and search

Tech stack:
- Frontend - JS React
- Backend - Python FastAPI
- Server - uvicorn
- DB - SQLLite
- ORM - SQLAlchemy
- Docker

## Installation

### Frontend - React

To setup the environment variables in the React application, copy the .env.dist file and rename it to .env, then adjust the variables as needed

```sh
  yarn install
  yarn start
```

### Backend - External docker containers

Launch the docker container with the RabbitMQ server
```
  docker run -d -p 5672:5672 rabbitmq:3-management
```

Launch the docker container with the AI image content recognition tool
```
  docker run -it -p 5000:5000 quay.io/codait/max-image-caption-generator
```


### Backend - FastAPI
First, it is recommended to setup your python virtual environment : [venv](https://docs.python.org/3/library/venv.html)

Then, to setup the environment variables in the FastAPI application, copy the .env.dist file and rename it to .env, then adjust the variables as needed

Then, execute these commands :
```sh
  python -m pip install -r requirements.txt
  python -m uvicorn app.main:app --host 0.0.0.0 --port 80
```



