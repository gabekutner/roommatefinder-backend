<div align="center">
  <h1>
    UofU RoommateFinder
  </h1>
</div>



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
