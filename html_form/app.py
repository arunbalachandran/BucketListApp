from flask import Flask, request, render_template, json, redirect
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import session  # to stop unauthorized access
import os
import re
# for debugging only
import sys
email_validator = re.compile('[^@]+@[^@]+\.[^@]+')
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
mysql = MySQL()
# how to do this using files for production?
# is this it?
# here os.environ should represent the heroku environ
db_url = os.environ['CLEARDB_DATABASE_URL'].split('//')
app.config['MYSQL_DATABASE_USER'] = db_url[1].split(':')[0]
app.config['MYSQL_DATABASE_PASSWORD'] = db_url[1].split(':')[1].split('@')[0]
app.config['MYSQL_DATABASE_DB'] = db_url[1].split(':')[1].split('@')[1].split('/')[1].split('?')[0]
app.config['MYSQL_DATABASE_HOST'] = db_url[1].split(':')[1].split('@')[1].split('/')[0]
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _hashed_password = generate_password_hash(_password)
    cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
    data = cursor.fetchall()

    if len(data) is 0:
        conn.commit()
        return json.dumps({'message': 'User created successfully !'})
    else:
        return json.dumps({'error': str(data[0])})

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        # different from the cursor used for signup
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()
        if (len(data) > 0):
            if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html', error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html', error = 'Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html', error = str(e))
    # close the cursor that we created only for this database
    finally:
        cursor.close()
        con.close()

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error = 'Unauthorized Access')
    return render_template('userHome.html')

@app.route('/showAddWish')
def showAddWish():
    return render_template('addWish.html')

@app.route('/addWish', methods=['POST'])
def addWish():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addWish', (_title, _description, _user))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return redirect('/userHome')
            else:
                return render_template('error.html', error = 'An error occurred!')
        else:
            return render_template('error.html', error = 'Unauthorized Access')

    except Exception as e:
        return render_template('error.html', error = str(e))

    finally:
        cursor.close()
        conn.close()

@app.route('/getWish')
def getWish():
    try:
        if session.get('user'):
            _user = session.get('user')
            # Connect to MySQL and fetch data
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetWishByUser',(_user,))
            wishes = cursor.fetchall()
            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                    'Id': wish[0],
                    'Title': wish[1],
                    'Description': wish[2],
                    'Date': wish[4]}
                wishes_dict.append(wish_dict)
            print wishes_dict
            print 'py code here'
            sys.stdout.flush()
            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='localhost', port='5000')
    print 'app is done here'
    sys.stdout.flush()
    # does the app reach here
    cursor.close()
    conn.close()
