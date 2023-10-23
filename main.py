
#-----ALL IMPORTS-----#
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import Database.database as db
import sqlite3
import subprocess
from tkinter import ttk

#-----> WINDOW CREATION
root = Tk()
root.title("Internet Broadband Management")
root.geometry("1000x700")
root.config(bg="#F0F8FF")


#-----> IMAGE IMPORT
image = Image.open("img.png")
image = ImageTk.PhotoImage(image)



#-----> PREDEFINED VARIABLES
var = StringVar(value="25mbps")
var_duration = IntVar(value=1)

password_verified = BooleanVar()

#-----> STYLING AND PREDEFINED VARIABLES

client_data = {
    "name": "",
    "username": "",
    "password": "",
    "phone_number": "",
    "address": "",
    "internet_plan": "",
    "duration": 0,
}

button_style = {
    "bg": "#007FFF",
    "fg": "#F0F8FF",
    "font": ("Arial", 14),
    "relief": "raised",
    "padx": 20,
    "pady": 10,
}

small_button = {
    "bg": "#007FFF",
    "fg": "#F0F8FF",
    "font": ("Arial", 12),
    "relief": "raised",
    "padx": 10,
    "pady": 5,
}

internet_plans = {
    "25mbps": 299,
    "50mbps": 499,
    "75mbps": 999,
    "100mbps": 1499,
}

client_data = {
    "name": "",
    "username": "",
    "password": "",
    "phone_number": "",
    "address": "",
    "internet_plan": "",
    "duration": 0,
}

back_button_style = {

    "bg": "#007FFF",
    "fg": "#F0F8FF",
    "font": ("Arial", 10, "bold"),
    "relief": "raised",
    "padx": 7,
    "pady": 5,
}

select_plan_frame = Frame(bg="#F0F8FF")

db.create_tables()

#-----> EXIT PROMPTING
def on_closing():
    if messagebox.askokcancel("Quit", "Are you sure you want to exit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)


#-------------------------- HOME --------------------------------------

def home():
    homeFrame = Frame(bg="#F0F8FF")
    homeFrame.place(x=0, y=0, width=1000, height=700)

    heading = Label(homeFrame, text="Internet Broadband Management", bg="#F0F8FF", font=("Arial", 24), fg="#007FFF", pady=20)
    heading.pack()

    adminLoginButton = Button(homeFrame, text="Admin Login", **button_style, command=adminlog)
    adminLoginButton.place(x=370, y=150, width=120, height=65)

    clientLoginButton = Button(homeFrame, text="Client Login", **button_style, command=clientlog)
    clientLoginButton.place(x=510, y=150, width=120, height=65)

    signup_label = Button(homeFrame, text="New Client? Signup", font=("Arial", 10), bg="#F0F8FF", fg="#007FFF", bd=0, cursor="hand2", command=client_signup)
    signup_label.place(x=435, y=225)

    image_label = Label(homeFrame, image=image, bg="#F0F8FF")
    image_label.image = image
    image_label.place(x=225, y=300, height=400)

#----------------------- ADMIN LOGIN -----------------------------------


#-----> ADMIN LOGIN PAGE STARTS HERE
def adminlog():
    adminLogFrame = Frame(bg="#F0F8FF")
    adminLogFrame.place(x=0, y=0, width=1000, height=700)

    heading = Label(adminLogFrame, text="Input Your Admin Credentials", font=("Arial", 24), bg="#F0F8FF", fg="#007FFF", pady=20)
    heading.pack()

    username_label = Label(adminLogFrame, text="Enter Username", bg="#F0F8FF", font=("Arial", 12))
    username_label.pack()
    usernameEntry = Entry(adminLogFrame, font=("Arial", 12))
    usernameEntry.pack()

    password_label = Label(adminLogFrame, text="Enter Password", bg="#F0F8FF", font=("Arial", 12))
    password_label.pack()
    passwordEntry = Entry(adminLogFrame, show="*", font=("Arial", 12))
    passwordEntry.pack()

    def login_admin():
        username = usernameEntry.get()
        password = passwordEntry.get()
        admin = admin_login(username, password)

        if admin:
            # Admin is logged in successfully
            messagebox.showinfo("Success", "Admin logged in successfully!")
            admin_interface()  # Open the admin interface
        else:
            # Invalid admin credentials
            messagebox.showerror("Error", "Invalid admin credentials!")

    LoginButton = Button(adminLogFrame, text="Login", **small_button, command=login_admin)
    LoginButton.pack(pady=12)

    backButton = Button(adminLogFrame, text="Back", command=home, **back_button_style)
    backButton.place(x=2, y=3)

#-----> ADMIN LOGIN PAGE ENDS HERE

#-----> ADMIN INTERFACE STARTS HERE

def admin_interface():
    adminInterfaceFrame = Frame(bg="#F0F8FF")
    adminInterfaceFrame.place(x=0, y=0, width=1000, height=700)

    title = Label(adminInterfaceFrame, text="Admin Dashboard", bg="#F0F8FF", font=("Arial", 24), fg="#007FFF", pady=20)
    title.pack()

    tree = ttk.Treeview(adminInterfaceFrame, columns=(1, 2, 3, 4, 5, 6, 7), show="headings")
    tree.heading("#1", text="Username")
    tree.heading("#2", text="Password")
    tree.heading("#3", text="Phone Number")
    tree.heading("#4", text="Payment Done")
    tree.heading("#5", text="Internet Plan")
    tree.heading("#6", text="Address")
    tree.heading("#7", text="Duration In Months")
    tree.column("#1", anchor=CENTER, width=100)
    tree.column("#2", anchor=CENTER, width=100)
    tree.column("#3", anchor=CENTER, width=100)
    tree.column("#4", anchor=CENTER, width=100)
    tree.column("#5", anchor=CENTER, width=100)
    tree.column("#6", anchor=CENTER, width=100)
    tree.column("#7", anchor=CENTER, width=100)
    tree.pack()

    clients = db.get_all_clients()
    for client in clients:
        tree.insert("", "end", values=(client[1], client[2], client[5], client[6], client[7], client[4], client[8]))

    logout_button = Button(adminInterfaceFrame, text="Logout", command=home, **button_style)
    logout_button.place(x=450, y=500)

    tree.tag_configure("column_title", font=("Arial", 12, "bold"))
    for col in tree["columns"]:
        tree.heading(col, text=tree.heading(col)["text"], anchor=CENTER, command=lambda c=col: sort_treeview(tree, c), image="")
        tree.heading(col, text=tree.heading(col)["text"], anchor=CENTER, command=lambda c=col: sort_treeview(tree, c))
        tree.tag_bind(col, "<Button-1>", lambda e, col=col: tree.heading(col, text=tree.heading(col)["text"] + " ▲"))
        tree.tag_bind(col, "<Button-1>", lambda e, col=col: tree.heading(col, text=tree.heading(col)["text"] + " ▼"))
        tree.tag_add("column_title", col)

def sort_treeview(tree, col):
    """Sort the given Treeview column alphabetically."""
    items = [(tree.set(item, col), item) for item in tree.get_children('')]
    items.sort()
    for index, (val, item) in enumerate(items):
        tree.move(item, '', index)

#-----> ADMIN INTERFACE ENDS HERE


#----------------------- CLIENT LOGIN ----------------------------------

#-----> CLIENT LOGIN PAGE STARTS HERE
def clientlog():
    clientLogFrame = Frame(bg="#F0F8FF")
    clientLogFrame.place(x=0, y=0, width=1000, height=700)

    heading = Label(clientLogFrame, text="Input Your Credentials", bg="#F0F8FF",  font=("Arial", 24),  fg="#007FFF", pady=20)
    heading.pack()

    username_label = Label(clientLogFrame, text="Enter Username",bg="#F0F8FF", font=("Arial", 12))
    username_label.pack()
    usernameEntry = Entry(clientLogFrame, font=("Arial", 12))
    usernameEntry.pack()

    password_label = Label(clientLogFrame, text="Enter Password",bg="#F0F8FF", font=("Arial", 12))
    password_label.pack()
    passwordEntry = Entry(clientLogFrame, show="*", font=("Arial", 12))
    passwordEntry.pack()

    forgot_password_label = Label(clientLogFrame, text="Forgot Password?", bg="#F0F8FF", font=("Arial", 10), fg="#007FFF", cursor="hand2")
    forgot_password_label.pack()
    forgot_password_label.bind("<Button-1>", lambda e: reset_password())

    def login_client():
        username = usernameEntry.get()
        password = passwordEntry.get()
        client_login(username, password)

    LoginButton = Button(clientLogFrame, text="Login", **small_button, command=login_client)
    LoginButton.pack(pady=12)

    backButton = Button(clientLogFrame, text="Back", command=home, **back_button_style)
    backButton.place(x=2, y=3)

#-----> CLIENT LOGIN PAGE ENDS HERE

#-----> CHANGE PLAN STARTS HERE
def change_plan(user,intplan,dur):
    change_plan_frame = Frame(bg="#F0F8FF")
    change_plan_frame.place(x=0, y=0, width=1000, height=700)

    username=user
    var = StringVar()
    var_duration = IntVar()
    var.set(intplan)
    var_duration.set(dur)

    internet_plan_label = Label(change_plan_frame, text="Select Internet Plan:")
    internet_plan_label.pack()

    for plan, price in internet_plans.items():
        plan_radio = Radiobutton(change_plan_frame, text=f"{plan} (₹{price}/month)", variable=var, value=plan)
        plan_radio.pack()

    duration_label = Label(change_plan_frame, text="Select Duration (in months):")
    duration_label.pack()

    for duration in [1, 3, 6, 12]:
        duration_radio = Radiobutton(change_plan_frame, text=f"{duration} Months", variable=var_duration, value=duration)
        duration_radio.pack()

    save_button = Button(change_plan_frame, text="Save Changes", command=lambda:(save_changes_logout(user,var.get(),var_duration.get())), **button_style)
    save_button.pack(pady=12)

def save_changes(z,x,y):
        selected_plan = x
        duration = y

        username = z
        db.update_internet_plan_duration(username, selected_plan, duration)
        messagebox.showinfo("Changes Saved", "Internet plan and duration have been updated.")

def save_changes_logout(z,x,y):
    
    save_changes(z,x,y)
    messagebox.showinfo("Logged Out", "You are logged out ! Please log in again.")
    home()

#-----> CHANGE PLAN ENDS HERE

#-----> CLIENT INTERFACE STARTS HERE

def client_interface(client_data):
    clientInterfaceFrame = Frame(bg="#F0F8FF")
    clientInterfaceFrame.place(x=0, y=0, width=1000, height=700)

    title = Label(clientInterfaceFrame, text="Client Dashboard", bg="#F0F8FF", font=("Arial", 24), fg="#007FFF", pady=20)
    title.pack()

    invoice_frame = Frame(clientInterfaceFrame, bg="#F0F8FF")
    invoice_frame.pack()

    username_label = Label(invoice_frame, text="Username:", font=("Arial", 16), bg="#F0F8FF", anchor="w")
    username_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
    username_value = Label(invoice_frame, text=client_data["username"], font=("Arial", 16), bg="#F0F8FF", anchor="w")
    username_value.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    password_label = Label(invoice_frame, text="Password:", font=("Arial", 16), bg="#F0F8FF", anchor="w")
    password_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
    password_value = Label(invoice_frame, text=client_data["password"], font=("Arial", 16), bg="#F0F8FF", anchor="w")
    password_value.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    internet_plan_label = Label(invoice_frame, text="Internet Plan:", font=("Arial", 16), bg="#F0F8FF", anchor="w")
    internet_plan_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
    internet_plan_value = Label(invoice_frame, text=client_data["internet_plan"], font=("Arial", 16), bg="#F0F8FF", anchor="w")
    internet_plan_value.grid(row=2, column=1, padx=20, pady=10, sticky="w")

    duration_label = Label(invoice_frame, text="Duration of Plan:", font=("Arial", 16), bg="#F0F8FF", anchor="w")
    duration_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
    duration_value = Label(invoice_frame, text=f"{client_data['duration']} months", font=("Arial", 16), bg="#F0F8FF", anchor="w")
    duration_value.grid(row=3, column=1, padx=20, pady=10, sticky="w")

    total_cost_label = Label(invoice_frame, text="Amount Paid:", font=("Arial", 16), bg="#F0F8FF", anchor="w")
    total_cost_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
    total_cost_value = Label(invoice_frame, text=f"₹{calculate_total_cost(client_data):.2f}", font=("Arial", 16), bg="#F0F8FF", anchor="w")
    total_cost_value.grid(row=4, column=1, padx=20, pady=10, sticky="w")

    change_plan_button = Button(invoice_frame, text="Change Internet Plan", command=lambda:(change_plan(client_data["username"],client_data["internet_plan"],client_data["duration"])), **small_button)
    change_plan_button.grid(row=5, column=1, padx=20, pady=10)

    logout_button = Button(clientInterfaceFrame, text="Logout", command=home, **button_style)
    logout_button.place(x=450, y=500)

def calculate_total_cost(client_data):
    selected_plan = client_data["internet_plan"]
    duration = client_data["duration"]
    return internet_plans[selected_plan] * duration

#-----> CLIENT INTERFACE ENDS HERE

#------> RESET PASSWORD FRAME STARTS HERE
def reset_password():
    resetPasswordFrame = Frame(bg="#F0F8FF")
    resetPasswordFrame.place(x=0, y=0, width=1000, height=700)

    phone_number_label = Label(resetPasswordFrame, text="Phone Number:", bg="#F0F8FF", font=("Arial", 12))
    phone_number_label.pack()
    phone_number_entry = Entry(resetPasswordFrame, font=("Arial", 12))
    phone_number_entry.pack()

    new_password_label = Label(resetPasswordFrame, text="New Password:", bg="#F0F8FF", font=("Arial", 12))
    new_password_label.pack()
    new_password_entry = Entry(resetPasswordFrame, show="*", font=("Arial", 12))
    new_password_entry.pack()

    def change_password():
        phone_number = phone_number_entry.get()
        new_password = new_password_entry.get()

        client = db.get_client_by_phone_number(phone_number)

        if client is not None: 
            username = client["username"]  
            db.update_password(username, new_password)
            messagebox.showinfo("Password Updated", "Your password has been updated.")
        else:
            messagebox.showerror("Phone Number Not Found", "Phone number not found in the database.")


    change_password_button = Button(resetPasswordFrame, text="Change Password", **small_button, command=change_password)
    change_password_button.pack(pady=12)

    back_button = Button(resetPasswordFrame, text="Back to Login", command=clientlog, **back_button_style)
    back_button.place(x=2, y=3)

#-----> RESET PASSWORD FRAME ENDS HERE


#---------------------- CLIENT SIGNUP ------------------------------------

#-----> CLIENT SIGNUP PAGE STARTS HERE
def client_signup():
    clientSignupFrame = Frame(bg="#F0F8FF")
    clientSignupFrame.place(x=0, y=0, width=1000, height=700)

    def create_account():
        name = name_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        phone_number = phone_number_entry.get()
        address = address_entry.get()

        if not phone_number.isdigit():
            messagebox.showerror("Invalid Phone Number", "Phone number should contain only integers.")
            return  

        selected_plan = var.get()
        duration = var_duration.get()

        db.add_client(username, password, name, address, phone_number, selected_plan, duration, 0.0)

        client_data["name"] = name
        client_data["username"] = username
        client_data["password"] = password
        client_data["phone_number"] = phone_number
        client_data["address"] = address
        client_data["internet_plan"] = selected_plan
        client_data["duration"] = duration

        clientSignupFrame.place_forget() 
        select_plan() 

    heading = Label(clientSignupFrame, text="Client Signup - Step 1", bg="#F0F8FF", font=("Arial", 24), fg="#007FFF", pady=20)
    heading.pack()

    name_label = Label(clientSignupFrame, text="Enter Your Name", bg="#F0F8FF", font=("Arial", 12))
    name_label.pack()
    name_entry = Entry(clientSignupFrame, font=("Arial", 12))
    name_entry.pack()

    username_label = Label(clientSignupFrame, text="Create Username", bg="#F0F8FF", font=("Arial", 12))
    username_label.pack()
    username_entry = Entry(clientSignupFrame, font=("Arial", 12))
    username_entry.pack()

    password_label = Label(clientSignupFrame, text="Create Password", bg="#F0F8FF", font=("Arial", 12))
    password_label.pack()
    password_entry = Entry(clientSignupFrame, show="*", font=("Arial", 12))
    password_entry.pack()

    phone_number_label = Label(clientSignupFrame, text="Enter Your Phone Number", bg="#F0F8FF", font=("Arial", 12))
    phone_number_label.pack()
    
    def validate_phone_number_input(action, value_if_allowed):
        if action == '1':
            if value_if_allowed.isdigit() or value_if_allowed == "":
                return True
            else:
                return False
        return True
    
    phone_number_entry = Entry(clientSignupFrame, font=("Arial", 12), validate="key")
    phone_number_entry.config(validatecommand=(phone_number_entry.register(validate_phone_number_input), '%d', '%P'))
    phone_number_entry.pack()

    address_label = Label(clientSignupFrame, text="Enter Your Address", bg="#F0F8FF", font=("Arial", 12))
    address_label.pack()
    address_entry = Entry(clientSignupFrame, font=("Arial", 12))
    address_entry.pack()

    create_account_button = Button(clientSignupFrame, text="Create Account", **small_button, command=create_account)
    create_account_button.pack(pady=12)

    back_button = Button(clientSignupFrame, text="Back", command=home, **back_button_style)
    back_button.place(x=2, y=3)

 #-----> CLIENTS SIGNUP PAGE ENDS HERE

#-----> CLIENT SIGNUP PAGE ENDS HERE
#-----> PLAN SELECTION FOR CLIENT SIGNUP STARTS HERE
def select_plan():
    select_plan_frame = Frame(bg="#F0F8FF")
    select_plan_frame.place(x=0, y=0, width=1000, height=700)

    def calculate_total_cost():
        selected_plan = var.get()
        duration = var_duration.get()
        result= internet_plans[selected_plan]*duration
        total_cost_label.config(text=f"Total Cost: ₹{internet_plans[selected_plan] * duration:.2f}")

    heading = Label(select_plan_frame, text="Client Signup - Step 2", bg="#F0F8FF", font=("Arial", 24), fg="#007FFF", pady=20)
    heading.pack()

    internet_plan_label = Label(select_plan_frame, text="Select Internet Plan", bg="#F0F8FF", font=("Arial", 12))
    internet_plan_label.pack()

    for plan, price in internet_plans.items():
        plan_radio = Radiobutton(select_plan_frame, text=f"{plan} (₹{price}/month)", variable=var, value=plan, bg="#F0F8FF", font=("Arial", 12))
        plan_radio.pack()

    duration_label = Label(select_plan_frame, text="Select Duration of Plan", bg="#F0F8FF", font=("Arial", 12))
    duration_label.pack()

    duration_radio_1 = Radiobutton(select_plan_frame, text="1 Month", variable=var_duration, value=1, bg="#F0F8FF", font=("Arial", 12))
    duration_radio_3 = Radiobutton(select_plan_frame, text="3 Months", variable=var_duration, value=3, bg="#F0F8FF", font=("Arial", 12))
    duration_radio_6 = Radiobutton(select_plan_frame, text="6 Months", variable=var_duration, value=6, bg="#F0F8FF", font=("Arial", 12))
    duration_radio_12 = Radiobutton(select_plan_frame, text="12 Months", variable=var_duration, value=12, bg="#F0F8FF", font=("Arial", 12))

    duration_radio_1.pack()
    duration_radio_3.pack()
    duration_radio_6.pack()
    duration_radio_12.pack()

    total_cost_label = Label(select_plan_frame, text="Total Cost: ₹0.00", bg="#F0F8FF", font=("Arial", 12))
    total_cost_label.pack()

    calculate_cost_button = Button(select_plan_frame, text="Calculate Total Cost", **small_button, command=calculate_total_cost)
    calculate_cost_button.pack(pady=12)

    pay_button = Button(select_plan_frame, text="Pay", **small_button, command=pay_and_return)
    pay_button.pack(pady=12)

    back_button = Button(select_plan_frame, text="Cancel", command=not_paid_home, **back_button_style)
    back_button.place(x=2, y=3)

    home_button = Button(select_plan_frame, text="Home", command=home, **back_button_style)
    home_button.pack()

    client_data = db.get_client_data(client_data["username"])
    current_plan = client_data["internet_plan"]
    current_duration = client_data["duration"]

    var.set(current_plan)
    var_duration.set(current_duration)

#-----> PLAN SELECTION FOR CLIENT SIGNUP ENDS HERE
#-------------- DATABASE OPERATIONS AND FUNCTIONS-------------------------

def update_client_data():
    global client_data
    if client_data:
        # Update client data in the database using functions from database.py
        db.update_client(client_data)

def pay():
    selected_plan = var.get()
    duration = var_duration.get()
    total_cost = internet_plans[selected_plan] * duration

    # Create the message with corrected grammar
    message = f"You have paid ₹{total_cost:.2f} and selected the {selected_plan} plan for {duration} months."

    # Update the payment_done field in the database
    db.update_payment_done(client_data["username"], total_cost)
    # Update the internet_plan and duration in the database
    db.update_internet_plan_duration(client_data["username"], selected_plan, duration)

    # Show the message in a message box
    messagebox.showinfo("Payment Successful", message)
    update_client_data()

def not_paid():
    selected_plan = "Not Selected"
    duration = "Not Selected"
    total_cost = 0.0

    db.update_payment_done(client_data["username"], total_cost)
    db.update_internet_plan_duration(client_data["username"], selected_plan, duration)

    messagebox.showinfo("Process Cancelled", "You have not selected any plan")
    update_client_data()

def admin_login(username, password):
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM admins WHERE username = ? AND password = ?', (username, password))
    admin = cursor.fetchone()
    connection.close()
    return admin  

def client_registration(name, username, password, phone_number):
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO clients (name, username, password, phone_number) VALUES (?, ?, ?, ?)', (name, username, password, phone_number))
    connection.commit()
    connection.close()
    messagebox.showinfo("Success", "Client registered successfully!")

def client_login(username, password):
    if client_credentials_are_valid(username, password):
        client_data = db.get_client_data(username)

        if client_data:
            client_interface(client_data)
        else:
            messagebox.showerror("Error", "Failed to retrieve client data.")
    else:
        messagebox.showerror("Error", "Invalid credentials!")

def client_credentials_are_valid(username, password):
    connection = sqlite3.connect('broadband_management.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM clients WHERE username = ? AND password = ?', (username, password))
    client = cursor.fetchone()
    connection.close()
    
    return client is not None

def pay_and_return():
    pay()
    home()

def not_paid_home():
    home()
    not_paid()

#-----> MAINLOOP STATEMENT
home()
root.mainloop()


