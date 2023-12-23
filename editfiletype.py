from tkinter import *
import mysql.connector
from connectdb import dbhost, dbname, dbpass, dbuser
import datetime
from loghandler import add_log_event
from tkinter import messagebox

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

def add_error():
    messagebox.showerror("File Type Found", "This file type already exists")

def add_data():
    new_filetype = filetype.get()
    mycursor.execute("select * from filetype where fileTypeName = %s", [new_filetype, ])
    result = mycursor.fetchall()
    if result:
        add_error()
    else:
        sql = "insert into filetype (fileTypeName) values(%s)"
        value = (new_filetype, )
        mycursor.execute(sql, value)
        db.commit()
        new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "event": "New File Type Added Successful"}
        add_log_event(new_event)
        messagebox.showinfo("File Type Added", "The New File Type is Added")
        root1.destroy()
        refresh()
    
def add_data_display():
    global root1
    root1 = Toplevel(root)
    root1.geometry("400x300")
    Label(root1, text="Add New File Type", font="bold", bg="grey", fg="black", height=3).grid(row=0, columnspan=3, sticky="ew")
    Label(root1, text="").grid(row=1, column=0)
    global filetype
    filetype = StringVar()
    Label(root1, text="File Type (eg: csv, txt): ", font="bold").grid(row=2, column=0)
    Entry(root1, textvariable=filetype).grid(row=2, column=1)
    Button(root1, text="Submit", width=8, height=1, command=add_data).grid(row=3, column=0)
   
def delete_data(filetypeID, filetype):
    mycursor.execute("delete from filetype where fileID = %s", (filetypeID, ))
    db.commit()
    new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "event": (filetype+ " deleted")}
    add_log_event(new_event)
    messagebox.showinfo("File Type Deleted", "The File Type is Deleted")
    refresh()

def refresh():
    for widget in inner_frame.winfo_children():
        widget.destroy()
        
    data = get_all_type()
    
    filetype_head = Label(inner_frame, text="File Type")
    filetype_head.grid(row=0, column=0)
    
    for i, column in enumerate(data):   #type: ignore
        filetypeID = column[0]
        filetype = column[1]
        
        id_label = Label(inner_frame, text=filetypeID)
        id_label.grid(row=i+1, column=0)
        filetype_label = Label(inner_frame, text=filetype)
        filetype_label.grid(row=i+1, column=1)
        
        delete_button = Button(inner_frame, text="Delete", fg="red", command=lambda fid=filetypeID, ft=filetype: delete_data(fid, ft))
        delete_button.grid(row=i+1, column=2)
    
    canvas.configure(scrollregion=canvas.bbox("all"))

def display():
    data = get_all_type()
    global root
    root = Tk()
    root.title("File Type")
    root.geometry("500x300")
    
    table_frame = Frame(root)
    table_frame.grid(row=0, column=0, sticky="nsew")
    
    global canvas
    canvas = Canvas(table_frame)
    scrollbar = Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.grid(row=0, column=0, sticky="nsew")
    
    global inner_frame
    inner_frame = Frame(canvas)
    canvas.create_window((0,0), window=inner_frame, anchor="nw")
    inner_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    
    filetype_head = Label(inner_frame, text="File Type")
    filetype_head.grid(row=0, column=0)
    
    for i, column in enumerate(data):   #type: ignore
        filetypeID = column[0]
        filetype = column[1]
        
        id_label = Label(inner_frame, text=filetypeID)
        id_label.grid(row=i+1, column=0)
        filetype_label = Label(inner_frame, text=filetype)
        filetype_label.grid(row=i+1, column=1)
        
        delete_button = Button(inner_frame, text="Delete", fg="red", command=lambda: delete_data(filetypeID, filetype))
        delete_button.grid(row=i+1, column=2)
        
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)
    
    add_button = Button(root, text="Add New File Type", command=add_data_display)
    add_button.grid(row=len(data)+1, column=0)  #type:ignore

    root.mainloop()
    
display()
