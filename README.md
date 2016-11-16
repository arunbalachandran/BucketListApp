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
6. And if you mess up, don't forget to check the server for filename changes that may go untracked because Mac and Windows platforms are case insensitive when it comes to files.
  ```
  heroku logs --source app
  heroku run bash
  ```
7. If you need to change the secret key.
  ```
  heroku config:unset SECRET_KEY
  ```
8. View the list of procedures using
  ```
  show procedure status;
  ```
9. Use pip to install from dependencies the requirements file.
  ```
  pip install -r requirements.txt
  ```
10. Add the venv and .env to the .gitignore file (use any text editor).
11. Create tables and stored procedures according to instructions in mysql_commands.txt
12. Test recursively using flask and heroku.
  ```
  python app.py
  heroku local
  ```
13. Push app to heroku and git.
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
