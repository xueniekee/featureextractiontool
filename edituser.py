from tkinter import *
import hashlib
import mysql.connector
from connectdb import dbhost, dbuser, dbpass, dbname
from loghandler import add_log_event
import datetime

db = mysql.connector.connect(
    host = dbhost(),
    user = dbuser(),
    password = dbpass(),
    database = dbname()
)
mycursor=db.cursor()
encrypt = hashlib.sha256()

def get_all_data():
    mycursor.execute("select * from user")
    data = mycursor.fetchall()
    return data
    
def delete_data(userID, username):
    mycursor.execute("delete from user where userID = %s", (userID, ))
    db.commit()
    new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "event": (username + " deleted")}
    add_log_event(new_event)
    refresh_data()
    
def refresh_data():
    for widget in table.winfo_children():
        widget.destroy()
    
    userID_head = Label(table, text='User ID')
    userID_head.grid(row=0, column=0)
    
    username_head = Label(table, text='Name')
    username_head.grid(row=0, column=1)
    
    userpass_head = Label(table, text='Password')
    userpass_head.grid(row=0, column=2)
    
    data = get_all_data()
    for i, column in enumerate(data):  #type: ignore
        userID = column[0]
        username = column[1]
        userpass = column[2]
        
        userID_label = Label(table, text=userID)
        userID_label.grid(row=i+1, column=0)
        username_label = Label(table, text=username)
        username_label.grid(row=i+1, column=1)
        userpass_label = Label(table, text=userpass)
        userpass_label.grid(row=i+1, column=2)

        delete_button = Button(table, text="Delete", command=lambda: delete_data(userID, username), fg="red")
        delete_button.grid(row=i+1, column=3)
    
def display():
    data = get_all_data()
    root = Tk()
    root.title("User Management")
    root.geometry("750x300")
    
    global table
    table = Frame(root)
    table.grid(row=1, column=0)
    
    userID_head = Label(table, text='User ID')
    userID_head.grid(row=0, column=0)
    
    username_head = Label(table, text='Name')
    username_head.grid(row=0, column=1)
    
    userpass_head = Label(table, text='Password')
    userpass_head.grid(row=0, column=2)
    
    for i, column in enumerate(data):  #type: ignore
        userID = column[0]
        username = column[1]
        userpass = column[2]
        
        userID_label = Label(table, text=userID)
        userID_label.grid(row=i+1, column=0)
        username_label = Label(table, text=username)
        username_label.grid(row=i+1, column=1)
        userpass_label = Label(table, text=userpass)
        userpass_label.grid(row=i+1, column=2)
        
        delete_button = Button(table, text="Delete", command=lambda: delete_data(userID, username), fg="red")
        delete_button.grid(row=i+1, column=3)
        
    root.mainloop()
    
display()