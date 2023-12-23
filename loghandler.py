from connectdb import dbhost, dbuser, dbpass, dbname
import mysql.connector
db = mysql.connector.connect(
    host = dbhost(),
    user = dbuser(),
    password = dbpass(),
    database = dbname()
)
mycursor=db.cursor()

log_event = []

def get_log_event():
    query = "select timestamp, user, event from securitylog"
    mycursor.execute(query)
    log_event = mycursor.fetchall()
    
    return log_event

row_count = mycursor.rowcount

def update_log_event(event):
    query = "insert into securitylog(timestamp, user, event) values (%s, %s, %s)"
    values = (event['timestamp'], event['user'], event['event'])
    mycursor.execute(query, values)
    db.commit()

def add_log_event(event):
    query = "insert into securitylog(timestamp, event) values (%s, %s)"
    values = (event['timestamp'], event['event'])
    mycursor.execute(query, values)
    db.commit()   
    