[**Roommatefinder**](https://github.com/gabekutner/roommatefinder-mobile) is a mobile app for finding college dorm roommates.

Built using: 
- [**React Native**](https://reactnative.dev)
- [**Django REST framework**](https://www.django-rest-framework.org/)
- [**Postgres**](https://www.postgresql.org/)
- [**Redis**](https://redis.io/)

This is the Django REST backend repository. Here's the link for the [**frontend**](https://github.com/gabekutner/roommatefinder-mobile).

##  Tech used
- 🐻 [**Zustand**](https://github.com/pmndrs/zustand)
- 🚩 [**react-native-fast-image**](https://github.com/DylanVann/react-native-fast-image)
- 🕹️ [**Font Awesome Icons**](https://fontawesome.com/)
- 🛩️ [**react-native-size-matters**](https://github.com/nirsky/react-native-size-matters)

## Preview
![preview](https://github.com/gabekutner/roommatefinder-mobile/blob/main/preview.png)

## Initialization

>NOTE: Some initialization requirements are still hardcoded: settings secrets (secret key, database configuration, channels configuration).

>This backend requires a Postgres database running on port 5432:5432 and a Redis server running on port 6379. Start a Postgres db in Docker and use `redis-server` for the Redis server.

Clone repository

```bash
git clone https://github.com/gabekutner/roommatefinder-backend.git
cd roommatefinder-backend
```

Create a virtual env

```bash
python3 -m venv env
source env/bin/activate
```

Install requirements

```bash
cd src/roommatefinder/requirements
python3 -m pip install -r _base.txt
```

And run

```bash
python3 manage.py runserver <ip:port>
```
