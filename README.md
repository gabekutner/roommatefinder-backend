<div align="center">
  <h1>
    UofU RoommateFinder
  </h1>
</div>

#### Table of Contents
* [Local Development](#local-development)
* [CI/CD Tempate](https://medium.com/intelligentmachines/github-actions-end-to-end-ci-cd-pipeline-for-django-5d48d6f00abf)

# Local Development
These settings should get you setup to work on your own machine 🚀

## Getting Started
1. Install `python3` : `brew install python3`
2. Install `redis` : `brew install redis`
3. Install `docker` : `brew install docker`

> I run use docker to run the postgres image instead of postgres.

## Setup Dev Environment

1. Pull the `postgres` image and run a container on port 5432.
```bash
>>> docker pull postgres
>>> docker run -e POSTGRES_PASSWORD=<password here> -p 5432:5432 postgres
```

2. Run `redis-server`, default port is `6379`.

> For this next step you can follow the next steps or use the `commands/dev-init.sh` command. They do the same thing, the script just saves time. Run it without parameters to see required parameters. They are the email for email backend, the four app passwords each as their own parameter, and finally the database stuff.
```bash
$ bash commands/dev-init.sh example.com 1234 1234 1234 1234 postgres
```

3. Create a `venv` in the top direcotry. Install project dependencies.
```bash
python3 -m venv env
source env/bin/activate

cd src/roommatefinder/requirements
python3 -m pip install -r _base.txt
```

4. For settings secrets, create a file called `sample_secrets.json` in `src/roommatefinder/roommatefinder/settings`. Add the following secrets:
```json
{
  "SECRET_KEY": "<django secret key>",
  "DATABASE_NAME": "<postgres db name>",
  "DATABASE_USER": "<postgres db user>",
  "DATABASE_PASSWORD": "<postgres db password>",
  "DATABASE_HOST": "localhost", 
  "DATABASE_PORT": 5432, 
  "EMAIL_HOST": "smtp.gmail.com",
  "EMAIL_PORT": 587, 
  "EMAIL_HOST_USER": "<your email>",
  "EMAIL_HOST_PASSWORD": "<passphrase>"
}
```

Run the server on your ip, port 8000
```bash
python3 manage.py runserver <your_ip_address>:8000
```