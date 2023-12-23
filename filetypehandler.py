from tkinter import *
import mysql.connector
from connectdb import dbhost, dbname, dbpass, dbuser

db = mysql.connector.connect(
    host = dbhost(),
    user = dbuser(),
    password = dbpass(),
    database = dbname()
)
mycursor = db.cursor()

def get_all_type():
    mycursor.execute("select * from filetype")
    data = mycursor.fetchall()
    return data

def get_file_type():
    mycursor.execute("select fileTypeName from filetype")
    data = [row[0] for row in mycursor.fetchall()]  #type: ignore
    return data