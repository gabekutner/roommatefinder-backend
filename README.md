<div align="center">
  <img src=".github/dormparty-red-app.png" height="200" alt="Dorm Party Icon">
  <h1>Dorm Party</h1>
</div>

#### Table of Contents
* [Project Description](#project-description)
* [Local Development](#local-development)
* [Running Tests](#running-tests)
<!-- * [Contributing Workflows](#contributing)
* [Contact](#contact) -->

### Additional Reading
* [API Details](contributing/API.md)
* [App Flow](contributing/FLOW.md)


# Project Description
This repository is the backend api for the Dorm Party mobile app. 
> Here's the link to the frontend repository: https://github.com/gabekutner/roommatefinder-mobile

The Dorm Party app will be published in Spring 2025 for freshmen at the University of Utah. 

# Local Development
### 🍴 Fork and Clone the Repo

First, yu need to fork the `roommatefinder-backend` repo. You can do this by clicking the Fork button on the top right corner of the repo. If you are new to forking, please watch this [YouTube Guide](https://www.youtube.com/watch?v=h8suY-Osn8Q) to get started.

Once forked, you can clone the repo by clicking the `Clone or Download` button on the top right corner of the forked repo. 

Please change the directory after cloning the repository using the `cd <folder-name>` command.

### ⬇️ Running the Development Server
To run the development server, make sure you have you have docker installed and setup on your machine. If you don't have docker read [this](https://docs.docker.com/desktop/).

Before running the docker commands edit the `.env.dev` file in the root directory and fill out the empty values. Keep in mind, if you change anything that is already set, you'll have to find where the variable is used and ensure it doesn't break the code. 

Here's a useful [website](https://djecrety.ir/) for generating your SECRET_KEY. For more on the `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` see [API Details](contributing/API.md). Also, change the `USE_SECRETS` value to False.

```.env
SECRET_KEY=""
DEBUG=True
DJANGO_SETTINGS_MODULE=roommatefinder.settings.dev
DATABASE_URL=postgres://myuser:mypassword@db:5432/mydatabase
REDIS_URL=redis://redis:6379/0
DATABASE_NAME="postgres"
DATABASE_USER="postgres"
DATABASE_PASSWORD="postgres123"
DATABASE_HOST="db"
DATABASE_PORT=5432
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_HOST_USER=""
EMAIL_HOST_PASSWORD=""

USE_SECRETS=True
```

After this, you're ready to run the docker actions. First, create the docker container.

```bash
docker-compose build
```

Then, before you run the container apply migrations.

```bash
docker-compose run web python3 roommatefinder/manage.py migrate
```

And create a superuser so that you can manage the database from `admin` panel. The identifier and password you choose are what you'll log in with when you look up that endpoint.

```bash
docker-compose run web python3 roommatefinder/manage.py createsuperuser
```

Finally, run the docker container. 

```bash
docker-compose up
```

To see the api and to connect to it from the mobile app, go to your Wi-Fi settings and find your IP address. If your IP is `10.0.0.49`, then you can find the api at this address: `http://10.0.0.49:8000/`.

These instructions should get you set up ready to work on Dorm Party 🎉

# Running Tests
Running tests is really pretty simple, I keep bash scripts for doing this in the `commands` folder in the root directory. 

First, make sure you have `coverage` installed manually or you can pip install `test.txt` in the requirements folder.

Then run, 

```bash
bash commands/__tests__/run_tests_on_api.sh
```

To see how much of the repository those tests cover run,

```bash
bash commands/__tests__/manual_coverage.sh
``` 

Keep in mind this only runs tests on the `api` app, so files like `manage.py`, or the `wsgi` / `asgi files ` are not part of either of the above reports.

<!-- # Contributing
Thanks for taking the time, first of all! Second, contributing is really simple. Follow the installation steps and create a pull request. As far as finding issues to work on, issues with the `FirstIssue` label are good for starters. 

Find that here: https://github.com/gabekutner/roommatefinder-backend/labels/FirstIssue

# Contact
If you run into an issue, have a question, or anything else  -->
