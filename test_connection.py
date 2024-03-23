#!/usr/bin/python3
import mysql.connector

try:
    connection = mysql.connector.connect(
        user='hbnb_dev',
        password='hbnb_dev_pwd',
        host='localhost',
        database='hbnb_dev_db'
    )
    print("Connection successful!")
    connection.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")
