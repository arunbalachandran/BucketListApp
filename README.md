# flask_dev
Small projects that I code to learn flask.

## Installation and deployment
Create an app in heroku.
Create a cleardb addon for the app.
```
Give examples
```
Setup the Procfile, the app.py and the html files.
Set configuration variables in heroku and export them to a .env file which heroku
will use during deployment.
```
touch .env
heroku config:set SECRET_KEY=<your_secret_key>
heroku config:set CLEARDB_DATABASE_URL=<CLEARDB_DATABASE_URL>
heroku config:get CLEARDB_DATABASE_URL -s >> .env
heroku config:get SECRET_KEY -s >> .env
```
The second step would be unnecessary because heroku automatically adds the
CLEARDB_DATABASE_URL to the configuration.
And if you mess up ...
```
heroku config:unset SECRET_KEY
```
Use pip to install from dependencies the requirements file.
```
pip install -r requirements.txt
```
Add the venv and .env to the .gitignore file.
```
Give examples
```
Create tables and stored procedures according to instructions in mysql_commands.txt

Provide examples of project deployment.
## API Reference
Template

## Tests
Template

## Contributors
Me.

## License
Distributed under the MIT License.
