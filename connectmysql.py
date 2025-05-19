import mysql.connector

from config import host, user, password, db_name, port

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=db_name,
    port=port,
    auth_plugin = 'mysql_native_password',
)
cursor = connection.cursor(buffered = True)