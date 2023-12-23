from tkinter import *
from tkinter import messagebox
from connectdb import dbhost, dbuser, dbpass, dbname
import mysql.connector
import os
import time
import hashlib
import importlib
import registerlogin
from loghandler import update_log_event
import datetime

def hash_password(password, salt):
    hashed_pass = hashlib.sha256(password.encode()+salt.encode()).hexdigest()
    return hashed_pass

db = mysql.connector.connect(
    host = dbhost(), user = dbuser(), password = dbpass(), database = dbname()
)
mycursor=db.cursor()
    
def succ_destroy():
    succ.destroy()
    root1.destroy()
    root.destroy()
    importlib.reload(registerlogin)

def validate_password(password):
    if len(password) < 8:
        messagebox.showerror("Password Error", "Your password should have at least 8 characters")
        return False
    if not any (char.isdigit() for char in password):
        messagebox.showerror("Password Error", "Your password should contain numeric character(s)")
        return False
    
    special_char = "!@#$%^&*()_-+=[]{}|:;<,>.?/~"
    if not any(char in special_char for char in password):
        messagebox.showerror("Password Error", "Your password should contain special character(s)")
        return False
    
    return True
   
def empty_error():
    messagebox.showerror("Input Missing", "All fields are required...")

def username_error():
    messagebox.showerror("Used Username", "This username already used")

def usertype_error():
    messagebox.showerror("Unknown User Type", "Choose User Type")

def success():
    global succ
    succ = Toplevel(root1)
    succ.title("Success")
    succ.geometry("200x100")
    Label(succ, text="Registration successful...", fg="green", font="bold").pack()
    Label(succ, text="").pack()
    Button(succ, text="Ok", bg="grey", width=8, height=1, command=succ_destroy).pack()
    
def register_user():
    username_info = username.get()
    password_info = password.get()
    if username_info == "":
        empty_error()
    elif password_info == "":
        empty_error()
    else:
        if str(var.get()) == "2":
            sql_check = "select * from user where name = %s"
            mycursor.execute(sql_check, [username_info])
            namefound = mycursor.fetchall()
            if namefound:
                username_error()
            else:
                if validate_password(password_info) == False:
                    messagebox.showerror("Password Error", "Change your password")
                else:
                    encrypted_pass = hash_password(password_info, username_info)
                    sql = "insert into user(name, password) values(%s,%s)"
                    t = (username_info, encrypted_pass)
                    mycursor.execute(sql, t)
                    db.commit()
                    Label(root1, text="Successfully Registered").pack()
                    time.sleep(0.50)
                    success()
                    new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user": username_info, "event": "Register Successful"}
                    update_log_event(new_event)
        elif str(var.get()) == "1":
            sql_check = "select * from admin where adminName = %s"
            mycursor.execute(sql_check, [username_info])
            namefound = mycursor.fetchall()
            if namefound:
                username_error()
            else:
                if validate_password(password_info) == False:
                    messagebox.showerror("Password Error", "Change your password")
                else:
                    encrypted_pass = hash_password(password_info, username_info)
                    sql = "insert into admin (adminName, adminPassword) values(%s, %s)"
                    t = (username_info, encrypted_pass)
                    mycursor.execute(sql, t)
                    db.commit()
                    Label(root1, text="Successfully Registered").pack()
                    time.sleep(0.50)
                    success()   
                    new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user": username_info, "event": "Register Successful"}
                    update_log_event(new_event)  
        else:
            usertype_error()  
        
def registration():
    global root1
    root1 = Toplevel(root)
    root1.title("Registration Page")
    root1.geometry("300x300")
    global username
    global password
    Label(root1,text="Register your account",bg="grey",fg="black",font="bold",width=300).pack()
    username = StringVar()
    password = StringVar()
    Label(root1,text="").pack()
    Label(root1,text="Username :",font="bold").pack()
    Entry(root1,textvariable=username).pack()
    Label(root1, text="").pack()
    Label(root1, text="Password :").pack()
    Entry(root1, textvariable=password,show="*").pack()
    Label(root1, text="").pack()
    global var
    var = IntVar()
    RB1 = Radiobutton(root1, text="Admin", variable=var, value=1)
    RB1.pack()
    RB2 = Radiobutton(root1, text="User", variable=var, value=2)
    RB2.pack()
    Button(root1,text="Register",bg="red",command=register_user).pack()

def login():
    global root1
    root1 = Toplevel(root)
    root1.title("Login Page")
    root1.geometry("300x300")
    global username_varify
    global password_varify
    Label(root1, text="Login Page", bg="grey", fg="black", font="bold",width=300).pack()
    username_varify = StringVar()
    password_varify = StringVar()
    Label(root1, text="").pack()
    Label(root1, text="Username :", font="bold").pack()
    Entry(root1, textvariable=username_varify).pack()
    Label(root1, text="").pack()
    Label(root1, text="Password :").pack()
    Entry(root1, textvariable=password_varify, show="*").pack()
    Label(root1, text="").pack()
    Button(root1, text="Login as User", bg="red",command=loginuser_varify).pack()
    Label(root1, text="")
    Button(root1, text="Login as Admin", bg="grey", command=loginadmin_varify).pack()
    
def logg_destroy():
    new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user": user_varify, "event": "Logout Successful"}
    update_log_event(new_event)
    logg.destroy()
    root1.destroy()
    root.destroy()

def logged_admin():
    global logg
    logg = Toplevel(root)
    logg.title("Welcome")
    logg.geometry("300x200")
    Label(logg, text="Welcome {} ".format(username_varify.get()), fg="green", font="bold").pack()
    Label(logg, text="").pack()
    Button(logg, text="View / Edit Users", bg="grey", width=8, height=1, command=edit_user).pack()
    Button(logg, text="View Security Log", bg="grey", width=8, height=1, command=view_log).pack()
    Button(logg, text="Add File Type", bg="grey", width=8, height=1, command=edit_filetype).pack() 
    Button(logg, text="Log-Out", fg="red", width=8, height=1, command=logg_destroy).pack()

def logged():
    global logg
    logg = Toplevel(root)
    logg.title("Welcome")
    logg.geometry("300x200")
    Label(logg, text="Welcome {} ".format(username_varify.get()), fg="green", font="bold").pack()
    Label(logg, text="").pack()
    Button(logg, text="Change Password", width=13, height=1, command=change_pass).pack()
    Button(logg, text="Preprocess ONLY", width=13, height=1, command=preprocess).pack()
    Button(logg, text="Preprocess & Extract", width=13, height=1, command=upload).pack()
    Button(logg, text="Log-Out", fg="red", width=3, height=1, command=logg_destroy).pack()
    
def failed():
    messagebox.showerror("Invalid credentials", "Invalid username / password")

def failed_admin():
    messagebox.showerror("Invalid credentials", "Invalid username / password")
    
def loginadmin_varify():
    global user_varify
    user_varify = username_varify.get()
    pas_varify = password_varify.get()
    encrypt_pas_varify = hash_password(pas_varify, user_varify)
    sql = "select * from admin where adminName = %s and adminPassword = %s"
    mycursor.execute(sql, [(user_varify), (encrypt_pas_varify)])
    results = mycursor.fetchall()
    if results:
        for i in results:
            logged_admin()
            new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user": user_varify, "event": "Login Successful"}
            update_log_event(new_event)
            break
        else:
            failed_admin()
            new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user": user_varify, "event": "Login Failed"}
            update_log_event(new_event)

def loginuser_varify():
    global user_varify
    user_varify = username_varify.get()
    pas_varify = password_varify.get()
    encrypt_pas_varify = hash_password(pas_varify, user_varify)
    sql = "select * from user where name = %s and password = %s"
    mycursor.execute(sql,[(user_varify),(encrypt_pas_varify)])
    results = mycursor.fetchall()
    if results:
        for i in results:
            logged()
            new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user": user_varify, "event": "Login Successful"}
            update_log_event(new_event)
            break
        else:
            failed()
            new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user": user_varify, "event": "Login Failed"}
            update_log_event(new_event)

def view_log():
    os.system('python3 viewlog.py')

def edit_user():
    os.system('python3 edituser.py')

def upload():
    os.system('python3 upload.py')

def preprocess():
    os.system('python3 preprocess.py')
 
def edit_filetype():
    os.system('python3 editfiletype.py')
    
def change_pass():
    global root2
    root2 = Toplevel(root)
    root2.title("Change Password")
    global oldpass
    oldpass = StringVar()
    global newpass
    newpass = StringVar()
    global repeatpass
    repeatpass = StringVar()
    Label(root2, text="Old Password: ", font='bold').pack()
    Entry(root2, textvariable=oldpass, show="*").pack()
    Label(root2, text="New Password: ", font="bold").pack()
    Entry(root2, textvariable=newpass, show="*").pack()
    Button(root2, text="Change Password", bg="grey", width=9, height=1, command=change).pack()
    Button(root2, text="Cancel", bg="grey", width=8, height=1, command=change_pass_destroy).pack()

def change_pass_destroy():
    root2.destroy()
    
def change():
    username = username_varify.get()
    getoldpass = oldpass.get()
    encrypt_oldpass = hash_password(getoldpass, username)
    sql = "select * from user where name = %s and password = %s"
    mycursor.execute(sql,[(username),(encrypt_oldpass)])
    result = mycursor.fetchone()
    userID = int(result[0]) #type: ignore
    getnewpass = newpass.get()
    
    if result:
        if getoldpass == getnewpass:
            messagebox.showerror("Password Error", "Old password and new password are the same")
        else:
            encrypt_newpass = hash_password(getnewpass, username)
            print(encrypt_newpass)
            sql = "update user set password = %s where userID = %s"
            value = (encrypt_newpass, userID)
            mycursor.execute(sql, value)
            db.commit()
            new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user": user_varify, "event": "Password Changed"}
            update_log_event(new_event)
            succ_change_password()
    else:
        fail_change_password()
        new_event = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user": user_varify, "event": "Password Change Failed"}
        update_log_event(new_event)

def succ_change_password():
    global succ
    succ = Toplevel(root2)
    succ.title("Success")
    succ.geometry("200x100")
    Label(succ, text="Password Changed.", fg="green", font="bold").pack()
    Label(succ, text="").pack()
    Button(succ, text="Ok", bg="grey", width=8, height=1, command=succ_destroy).pack()
    
def fail_change_password():
    messagebox.showerror("Fail Changing Password", "Failed to change password")
    
def main_screen():
    global root
    root = Tk()
    root.title("Login")
    root.geometry("300x300")
    root.resizable(False, False)
    Label(root,text="Feature Extraction Tool",font="bold",bg="grey",fg="black",width=300, height=5).pack()
    Label(root,text="").pack()
    Button(root,text="Login",width="8",height="1",font="bold",command=login).pack()
    Label(root,text="").pack()
    Button(root, text="Registration",height="1",width="12",font="bold",command=registration).pack()

main_screen()
root.mainloop()    
