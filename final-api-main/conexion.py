from peewee import *

database= MySQLDatabase(
    'sistema_restaurante',
    user='root', password='',
    host='localhost', port=3306
)