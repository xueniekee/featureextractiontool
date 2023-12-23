from tkinter import *
from tkinter import messagebox
from loghandler import get_log_event
from loghandler import row_count
from connectdb import dbhost, dbuser, dbpass, dbname
import mysql.connector
from tkinter import ttk

db = mysql.connector.connect(
    host = dbhost(),
    user = dbuser(),
    password = dbpass(),
    database = dbname()
)
mycursor=db.cursor()

log_events = get_log_event()

def view_log(log_events):
    root = Tk()
    root.title("Security Log")
    
    log_frame = Frame(root)
    log_frame.grid(row=0, column=0, sticky="nsew")
    
    canvas = Canvas(log_frame)
    scrollbar = Scrollbar(log_frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.grid(row=0, column=0, sticky="nsew")
    
    inner_frame = Frame(canvas)
    canvas.create_window((0,0), window=inner_frame, anchor="nw")
    
    inner_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    
    timestamp_head = Label(inner_frame, text="Timestamp")
    timestamp_head.grid(row=0, column=0)
    user_head = Label(inner_frame, text="User")
    user_head.grid(row=0, column=1)
    event_head = Label(inner_frame, text="Event")
    event_head.grid(row=0, column=2)
    
    for i, column in enumerate(log_events): #type: ignore
        timestamp = column[0]
        user = column[1]
        event = column[2]
        
        timestamp_label = Label(inner_frame, text=timestamp)
        timestamp_label.grid(row=i+1, column=0)
        user_label = Label(inner_frame, text=user)
        user_label.grid(row=i+1, column=1)
        event_label = Label(inner_frame, text=event)
        event_label.grid(row=i+1, column=2)
        
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    log_frame.grid_rowconfigure(0, weight=1)
    log_frame.grid_columnconfigure(0, weight=1)

    root.mainloop()
    
view_log(log_events)