from flask import Flask
from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
 
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'bd_devfruit'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
 
conn = mysql.connect()
cursor =conn.cursor()

FLASK_APP='views.py'
FLASK_ENV='development'
DEBUG = True

