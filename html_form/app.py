from flask import Flask, request, render_template, json, redirect, jsonify
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import session  # to stop unauthorized access
import json
import os
# for debugging only
import sys

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
mysql = MySQL()
# this is the heroku environment
db_url = os.environ['CLEARDB_DATABASE_URL'].split('//')
app.config['MYSQL_DATABASE_USER'] = db_url[1].split(':')[0]
app.config['MYSQL_DATABASE_PASSWORD'] = db_url[1].split(':')[1].split('@')[0]
app.config['MYSQL_DATABASE_DB'] = db_url[1].split(':')[1].split('@')[1].split('/')[1].split('?')[0]
app.config['MYSQL_DATABASE_HOST'] = db_url[1].split(':')[1].split('@')[1].split('/')[0]
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    conn = mysql.connect()
    cursor = conn.cursor()
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _hashed_password = generate_password_hash(_password)
    # first verify if he/she doesn't exist
    cursor.callproc('sp_validateLogin', (_email,))
    data = cursor.fetchall()
    # user doesn't exist
    if (len(data) <= 0):
        cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
        data = cursor.fetchall()
        if len(data) == 0:
            conn.commit()
            return json.dumps({'success': 'User created successfully'}), 200, {'ContentType': 'application/json'}
        # problem in creation
        else:
            return json.dumps({'error': str(data[0])}), 409, {'ContentType': 'application/json'}
    # user (email id) already exists
    else:
        return json.dumps({'error': str(data[0])}), 409, {'ContentType':'application/json'}

    # always close connections
    cursor.close()
    conn.close()

@app.route('/showSignIn')
def showSignin():
    print 'heelo'
    sys.stdout.flush()
    return render_template('signin.html')

@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    error = 'Wrong email address or password'
    correct_user = 'Correct User'
    _username = request.form['inputEmail']
    _password = request.form['inputPassword']
    # checks for the existence of a user
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()
        if (len(data) > 0):
            if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]
                print 'successful validation'
                sys.stdout.flush()
                return json.dumps({'success': True}), 200, {'ContentType':'application/json'}
            # not a valid password
            else:
                print 'insuccessful validation'
                sys.stdout.flush()
                return json.dumps({'error': True}), 400, {'ContentType':'application/json'}

        # not a valid username
        else:
            print 'cosuccessful validation'
            sys.stdout.flush()
            return json.dumps({'error': True}), 400, {'ContentType':'application/json'}
        # close the cursor that we created only for this database
        cursor.close()
        conn.close()
    except Exception as err:
        print err, 'is the error'
        sys.stdout.flush()

@app.route('/userHome')
def userHome():
    print 'Now at userhome with variable', session.get('user')
    if session.get('user'):
        return render_template('userhome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')

@app.route('/showAddWish')
def showAddWish():
    return render_template('addwish.html')

@app.route('/addWish', methods=['POST'])
def addWish():
    if session.get('user'):
        _title = request.form['inputTitle']
        _description = request.form['inputDescription']
        _user = session.get('user')
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_addWish', (_title, _description, _user))
        data = cursor.fetchall()
        if len(data) == 0:
            conn.commit()
            return redirect('/userHome')
        else:
            return render_template('error.html', error='An error occurred!')
        cursor.close()
        conn.close()
    else:
        return render_template('error.html', error='Unauthorized Access')

    cursor.close()
    conn.close()

@app.route('/getWish')
def getWish():
    if session.get('user'):
        _user = session.get('user')
        # Connect to MySQL and fetch data
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_GetWishByUser',(_user,))
        wishes = cursor.fetchall()
        wishes_list = []
        for wish in wishes:
            wish_dict = {
                'Id': wish[0],
                'Title': wish[1],
                'Description': wish[2],
                'Date': str(wish[4])}   # to fix date time serialization error
            wishes_list.append(wish_dict)
        cursor.close()
        conn.close()
        return json.dumps(wishes_list)
    else:
        return render_template('error.html', error='Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run()
