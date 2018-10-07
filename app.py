from flask import Flask, request, session,escape,jsonify, make_response, redirect, abort, url_for ,json
from flask_sqlalchemy import SQLAlchemy
import uuid
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from functools import wraps
from passlib.hash import sha256_crypt
import itertools
import numpy as np
import base64


app = Flask(__name__)

app.config['SECRET_KEY'] = 'itissecretkey'
app.config['SQLALCHEMY_ECHO']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/abeersingh/Downloads/GREENELY_BACKEND_TEST/test_data_2018_05_28.db'

db = SQLAlchemy()
db.init_app(app)

# users class of users table in database file
class users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.TEXT)
    password = db.Column(db.TEXT)

# the very first function call
@app.route('/')
def hello():
    return redirect(url_for('login'))


# function to user log in
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('1.Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = users.query.filter_by(user_name=auth.username).first()

    if not user:
        return make_response('2.Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if (user.password == auth.password):
        token = jwt.encode({'user_id' : user.user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('3.Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})




# token to authenticate the logged in user
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            username = request.authorization.username
            connection = db.engine.raw_connection()
            cursor = connection.cursor()
            name = str(username)
            cursor.execute('SELECT * FROM users WHERE  user_name=?',(name, ))
            current_user = cursor.fetchone()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# Function to show the limits ENDPOINT of API of logged in user
@app.route('/limits', methods=['GET'])
@token_required
def getuserlimits(current_user):

    connection = db.engine.raw_connection()
    cursor = connection.cursor()

    cursor.execute('select min(months.consumption) from months WHERE months.user_id=?', (current_user[0],))
    minMonthsCon = cursor.fetchone()[0]

    cursor.execute('select max(months.consumption) from months WHERE months.user_id=?',(current_user[0],))
    maxMonthsCon = cursor.fetchone()[0]

    cursor.execute('select trim(min(months.timestamp),"00:00:00") from months WHERE months.user_id=?', (current_user[0],))
    minMonthsTimest = cursor.fetchone()[0]

    cursor.execute('select trim(max(months.timestamp),"00:00:00") from months WHERE months.user_id=?',(current_user[0],))
    maxMonthsTimest =cursor.fetchone()[0]

    cursor.execute('select min(months.temperature) from months WHERE months.user_id=?',(current_user[0],))
    minMonthsTemp =cursor.fetchone()[0]

    cursor.execute('select max(months.temperature) from months WHERE months.user_id=?',(current_user[0],))
    maxMonthsTemp =cursor.fetchone()[0]

    cursor.execute('select min(days.consumption) from days WHERE days.user_id=?', (current_user[0],))
    minDaysCons =cursor.fetchone()[0]

    cursor.execute('select max(days.consumption)  from days WHERE days.user_id =?', (current_user[0],))
    maxDaysCons =cursor.fetchone()[0]

    cursor.execute('select  trim(max(days.timestamp),"00:00:00")  from days WHERE days.user_id =?', (current_user[0],))
    maxDaysTimest =cursor.fetchone()[0]

    cursor.execute('select  trim(min(days.timestamp),"00:00:00")  from days WHERE days.user_id =?', (current_user[0],))
    minDaysTimest =cursor.fetchone()[0]

    cursor.execute('select  min(days.temperature)  from days WHERE days.user_id =?', (current_user[0],))
    minDaysTemp = cursor.fetchone()[0]

    cursor.execute('select  max(days.temperature)  from days WHERE days.user_id =?', (current_user[0],))
    maxDaysTemp =cursor.fetchone()[0]


    jsonObject = {
        "months": {
                    "timestamp": {
                        'minimum': minMonthsTimest,
                        'maximum': maxMonthsTimest
                    },

                    "consumption": {
                        "minimum": minMonthsCon,
                        "maximum": maxMonthsCon
                    },
                    "temperature": {
                        "minimum": minMonthsTemp,
                        "maximum": maxMonthsTemp
                    }
                },
                "days": {
                    "timestamp": {
                        "minimum": minDaysTimest,
                        "maximum": maxDaysTimest
                    },
                    "consumption": {
                        "minimum": minDaysCons,
                        "maximum": maxDaysCons
                    },
                    "temperature": {
                        "minimum": minDaysTemp,
                        "maximum": maxDaysTemp
                    }
                }
    }

    return jsonify({'limits' : jsonObject})


# function to get the requested data on bases of user request
# Sample request = start=2014-03-01&count=8&resolution=M
@app.route('/data', methods=['GET'])
@token_required
def getreqdata(current_user):
    start = request.args.get('start')
    count = request.args.get('count')
    resolution = request.args.get('resolution')

    connection = db.engine.raw_connection()
    cursor = connection.cursor()

    output = []
    startdate=str(start)
    intcont=int(count)

    if resolution=="M":
        cursor.execute('select trim(months.timestamp, "00:00:00") , months.consumption, months.temperature from months where months.timestamp > ? and months.user_id=? limit ?,?' , (startdate,current_user[0],0,intcont))
        maxmonthstemp = cursor.fetchall()
        output=maxmonthstemp

    if resolution == "D":
        cursor.execute('select trim(days.timestamp, "00:00:00") , days.consumption, days.temperature from days where days.timestamp > ? and days.user_id=? limit ?,?', (startdate, current_user[0], 0, intcont))
        maxdaystemp = cursor.fetchall()
        output=maxdaystemp

    return jsonify({"data": output})


if __name__ == '__main__':
    app.run(debug=True)


