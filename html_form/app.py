from flask import Flask, request, render_template, json
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = '<enter_your_username>'
app.config['MYSQL_DATABASE_PASSWORD'] = '<enter_your_password>'
app.config['MYSQL_DATABASE_DB'] = '<enter_name_of_database>'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
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
    # create user code will be here !!
    # read the posted values from the UI
    # if request.method == 'POST':
    print 'here'
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _hashed_password = generate_password_hash(_password)
    cursor.callproc('sp_createUser',(_name, _email, _hashed_password))
    data = cursor.fetchall()

    if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'error':str(data[0])})

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
