<div align="center">
  <h1>
    UofU RoommateFinder
  </h1>
</div>

#### Table of Contents
* [Local Development](#local-development)

# Local Development
These settings should get you setup to work on your own machine 🚀

## Getting Started
1. Install `python3` : `brew install python3`
2. Install `redis` : `brew install redis`
3. (Optional) Install  `docker`
> I use `docker desktop`, but the CLI or a `postgres` database will work too.

## Setup Dev Environment
1. Run a `Postgres` image on port `5432`, using `docker` or `postgres`.
2. Run `redis-server`, default port is `6379`.
3. Create a `venv` in the top direcotry. Install project dependencies.
```bash
python3 -m venv env
source env/bin/activate

cd src/roommatefinder/requirements
python3 -m pip install -r _base.txt
```

Run the server on your ip, port 8000
```bash
python3 manage.py runserver <your_ip_address>:8000
```