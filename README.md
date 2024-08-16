<div align="center">
  <img src=".github/dormparty-red-app.png" height="200" alt="Dorm Party Icon">
  <h1>Dorm Party</h1>
</div>

An app where incoming college freshmen can find dorm roommates.
<br>
<br>
**This is just the backend of the app, if you're looking for the frontend: https://github.com/gabekutner/roommatefinder-frontend**

#### Table of Contents
* [Technologies Used](#technologies-used)
* [Getting Started](#getting-started)
* [Running Tests](#running-tests)
* [Project Structure](#project-structure)

# Technologies Used
* 🐍 [Django Rest Framework](https://www.django-rest-framework.org/)
* 🔴 [Redis](https://redis.io/)
* 🐘 [Postgres](https://www.postgresql.org/)
* 🐋 [Docker](https://www.docker.com/)
* [Daphne](https://github.com/django/daphne)
* [Django Channels](https://channels.readthedocs.io/en/latest/index.html)
* [Django Channels JWT Middleware](https://pypi.org/project/django-channels-jwt-auth-middleware/)

> Check out the live app! [Dorm Party Demo](https://gabekutner.github.io/roommatefinder-mobile/)

# Getting Started
### 🍴 Fork and Clone the Repo

1. **Fork the Repo:** Click the "Fork" button on the top right of this repository. If you're new to forking, check out this [YouTube Guide](https://www.youtube.com/watch?v=h8suY-Osn8Q).

2. **Clone Your Fork:** Click the Clone or Download button on the top right of your forked repo and clone it:

  ```bash
    git clone https://github.com/your-username/roommatefinder-backend.git
  ```

3. **Navigate to the Directory**:
   
  ```bash
    cd roommatefinder-backend
  ```

### ⬇️ Running the Development Server

1. **Install Docker**:
   
   Make sure Docker is installed and set up on your machine. If you don't have Docker, read [this guide](https://docs.docker.com/desktop/) for installation instructions.

2. **Configure Environment Variables**:

   Edit the `.env.dev` file in the root directory. You can generate a `SECRET_KEY` used this [website](https://djecrety.ir/). Set `USE_SECRETS` to `false`.
     * The `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are used for sending OTP verification codes via email. **In development, you can skip setting these variables unless you want to send emails.** To view OTP codes, access the Django admin panel (http://localhost:8000/admin/) and check the Profile model. If you want to work with emails, set `EMAIL_HOST_USER` with your email and generate an app password. See [this tutorial](https://www.youtube.com/watch?v=lSURGX0JHbA) for guidance.
  
   Example `.env.dev` file:

   ```ini
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
    USE_SECRETS=False
   ```

3. **Create a Sample Secrets File**:

   Create an empty `json` file in `src/roommatefinder/roommatefinder/settings` named `sample_secrets.json` with `{}` as its content.

   ```bash
    touch src/roommatefinder/roommatefinder/settings/sample_secrets.json
   ```

4. **Build the Docker Container**:

   ```bash
    docker-compose build
   ```

5. **Apply Migrations**:

   ```bash
    docker-compose run web python3 roommatefinder/manage.py migrate
   ```

6. **Create a Superuser**:

    This superuser will allow you to access the admin panel. Use the credentials you choose to log in.
  
    ```bash
      docker-compose run web python3 roommatefinder/manage.py createsuperuser
    ```

7. **Run the Docker Container**:

  ```bash
    docker-compose up
  ```

8. **Access the API**:

   Find your IP address in your Wi-Fi settings. If your IP is `10.0.0.49`, the API will be available at: `http://10.0.0.49:8000/`.

   > **Important**: Before publishing your code to GitHub, revert the `.env.dev` file by removing the values for `SECRET_KEY`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD`, and set `USE_SECRETS` to `true`.

<br>
These instructions should get you set up ready to work on Dorm Party 🎉


# Running Tests
To run tests, follow these steps:

1. **Install Coverage**:

  Ensure you have `coverage` installed. You can either install it manually or use `pip` to install from `test.txt` in the requirements folder.

2. **Run tests**:

   Execute the following script to run tests on the API:

   ```bash
     bash commands/__tests__/run_tests_on_api.sh
   ```

3. **Run Test Coverage**:

   To see how much of the repository is covered by tests, run:\

   ```bash
     bash commands/__tests__/manual_coverage.sh
   ```

> Note: This coverage report only includes the `api` app. Files like `manage.py`, and `wsgi` / `asgi` files are not part of the report.

# Project Structure

Most of the code is in the `src/roommatefinder/roommatefinder` folder. 

* **apps** : Where the `api` is defined and other `core` functionality.
* **settings** : App settings.

The `api` app is where all the endpoints and main functionality of the backend is defined.

* **internal** : Internal admin endpoints. Unaccessible by not admin users.
* **serializers** : Django Rest serializers used in the `views` folder.
* **tests** : Unit tests. One test file for every file in the `api` folder.
* **utils** : Utility functions for the app.
* **views** : API endpoints and backend logic!

* **managers.py** : A custom Profile User manager. Where the algorithm is defined.
* **consumers.py** : The consumer class for all Websocket connections.
* **models.py** : Models for all data.
