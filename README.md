# flask_dev
Small projects that I code to learn flask.

## Installation and deployment
1. Create an app in heroku. (Assuming you have a heroku account - free as of this writing)
2. Create a cleardb addon for the app.
3. Setup the Procfile, the app.py and the html files.
4. Set configuration variables in heroku and export them to a .env file which heroku will use during deployment.
```
touch .env
heroku config:set SECRET_KEY=<your_secret_key>
heroku config:set CLEARDB_DATABASE_URL=<CLEARDB_DATABASE_URL>
heroku config:get CLEARDB_DATABASE_URL -s >> .env
heroku config:get SECRET_KEY -s >> .env
export $(cat .env | xargs)
```
5. The second step would be unnecessary because heroku automatically adds the
CLEARDB_DATABASE_URL to the configuration.
And if you mess up ...
Don't forget to check the server for filename changes that may go untracked because
Mac and Windows platforms are case insensitive when it comes to files.
```
heroku config:unset SECRET_KEY
heroku logs --source app
heroku run bash
```
View list of procedures using
```
show procedure status;
```
6. Use pip to install from dependencies the requirements file.
```
pip install -r requirements.txt
```
7. Add the venv and .env to the .gitignore file.
8. Create tables and stored procedures according to instructions in mysql_commands.txt
9. Test recursively using ...
9. Push app to heroku and git.
```
git push origin master
git subtree push --prefix html_form heroku master
```

## API Reference
Template

## Tests
Template

## Contributors
Arun Balchandran (Me).

## License
Distributed under the MIT License.
