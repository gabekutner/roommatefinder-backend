<div align="center">
  <h1>
    RoommateFinder API
  </h1>
</div>

#### Table of Contents
* [Project Description](#project-description)
* [Local Development](#local-development)
* [Running Tests](#running-tests)

### Additional Reading
* [Code of Conduct](CODE_OF_CONDUCT.md)
* [Contributor License Agreement](contributing/CLA.md)

# Project Description
RoommateFinder API is the backend for the RoommateFinder mobile app. 
> Here's the link to the frontend repository: https://github.com/gabekutner/roommatefinder-mobile

These two repositories are going to be published as a mobile app for finding freshmen dorm roommates at the University of Utah. 

The api itself has three main endpoints:

* `/api/v1/profiles/`
* `/api/v1/photos/`
* `/api/v1/quizs/`

All endpoints are related to managing user profiles, the photos associated with these profiles and their roommate matching quizs.

These views are located in the `apps/api/views` folder [here](src/roommatefinder/roommatefinder/apps/api/views/). 

The api also has a websocket for messaging features located in the `apps/api/consumers` file. 

For more about the api, see [API Details](contributingGuides/API.md)


# Local Development
To run this api you need a `postgres` database running on port `5432` and a `redis` database running on port `6379`. The next steps explain how to this. Skip Step `3` if you can do by yourself.

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
python3 -m pip install -r dev.txt
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

Run the server on port 8000. If you're connecting this to the frontend, then run the server on `<your-ip>:8000` like below.
```bash
python3 manage.py runserver <your-ip>:8000
```

# Running Tests
Running tests is really pretty simple, I keep bash scripts for doing so in the `commands` folder at the top of the directory.

First, make sure you have `coverage` installed manually or you can pip install `test.txt` in the requirements folder.

After that simply run, 
```bash
bash commands/__tests__/run_tests_on_api.sh
```
from the top directory, and it'll run all the tests made so far in the repistory.

To see how much of the repository those tests cover run,
```bash
bash commands/__tests__/manual_coverage.sh
``` 

Keep in mind this simply runs tests on the `api` app, so most config files like `manage.py`, or the `wsgi` / `asgi files ` are not part of either of the above reports.