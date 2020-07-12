# Mumble recorder
  A simple mumble bot that can playback sound

## Dependencies
  Python, Postgresql, Mumble client and server
  opus library `brew install opus`

## Setup

1. Ensure the postgres server is running: `sudo service postgresql start`
2. Create a .env file at the root of this project and populate it with values for the following environment variables:
    ```
    export DB_URL=<postgres connection string>
    export MUMBLE_SERVER=<mumble server hostname>
    export MUMBLE_PORT=<mumble server port>
    export MUMBLE_PASSWORD=<mumble server password>
    export MUMBLE_USER=<mumble user name>
    ```
3. Install python package dependencies: `pip3 install -r requirements.txt`
4. Run database migrations: `alembic upgrade head`
5. Run the bot `./run_bot.sh`