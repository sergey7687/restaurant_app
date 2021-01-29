from flask import Flask
from flask_mysqldb import MySQL
from restapp.stock import Stock
import os

app = Flask('__name__', template_folder='restapp/templates', static_folder='restapp/static')
# config mysql
app.config['MYSQL HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Lindab123'
app.config['MYSQL_DB'] = 'restaurant_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

from restapp import routes
