from Tkinter import *
import tkMessageBox
import sqlite3
import bcrypt
import sys

# Best to put this with other initialization code
#root = Tk()
#root.title('Test Gui')

class MainFrame(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)

        self.label_1 = Label(self, text="Stuff will go here")
        self.label_1.grid(column=0)

        # Don't pack here. Do it when this frame is needed.
        #self.pack()

# Tk() only needs to be called once in the program
#login = Tk()
#login.title('Test Gui')

class LoginFrame(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label_1 = Label(self, text="User Login")
        self.label_2 = Label(self, text="Username")
        self.label_3 = Label(self, text="Password")

        self.entry_1 = Entry(self) # username box
        self.entry_1.focus_set() # Sets cursor automatically to username box
        self.entry_2 = Entry(self) # password box
        self.entry_2.config(show='*') #Hides password with '*' character

        self.label_1.grid(column=1)
        self.label_2.grid()
        self.label_3.grid()
        self.entry_1.grid(row=1, columnspan=2, column=1, padx=10, pady=5)
        self.entry_2.grid(row=2, columnspan=2, column=1, padx=10, pady=5)

        master.bind('<Return>', self.login_button_clicked) # allows ENTER button to be used instead of clicking 'login'
        self.log_button = Button(self, text="Login", command = self.login_button_clicked)
        self.log_button.grid(row=4, column=0, sticky=E, padx=(75,0))
        self.new_button = Button(self, text="New User", command = self.new_user_clicked)
        self.new_button.grid(row=4, column=1)

        #self.pack()

    def new_user_clicked(self):
        user = self.entry_1.get()
        userpass = self.entry_2.get()

        db = sqlite3.connect('credentials.db')
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials(username TEXT UNIQUE,
            password TEXT)''')
        used = False

        try:
            cursor.execute('''INSERT INTO credentials (username, password)
                            VALUES(?,?)''', (user, 'password'))
        except sqlite3.IntegrityError as msg:
            tkMessageBox.showerror('Error!', 'Username already in use!') # Shows error if username is already used.
            used = True

        if used == False:
            securepass = bcrypt.hashpw(userpass, bcrypt.gensalt())

            cursor.execute('''UPDATE credentials SET password =? WHERE username=?''',
                            (securepass, user))
            db.commit()
            tkMessageBox.showinfo('Success!', 'Successfully addded %s to the database!' % (user,))
            db.close()

    def login_button_clicked(self, *args):
        user = self.entry_1.get()
        userpass = self.entry_2.get()

        db = sqlite3.connect('credentials.db')
        db.text_factory = str
        cursor = db.cursor()

        cursor.execute('''SELECT password FROM credentials WHERE username=?''', (user,))
        check = cursor.fetchone()[0]

        if bcrypt.checkpw(userpass, check):
            print "Login Successfull..."
            # After the login is successful, destroy the login frame and pack the main frame
            l.destroy()
            m.pack()
            # Modify the geometry of the window if desired
            #root.geometry('%dx%d+%d+%d' % (w, h, x, y)) # --- end

        else:
            print "Login Failed..."
            tkMessageBox.showerror('Invalid Information!', 'Incorrect Username or Password!')

        db.close()


# Best to keep initialization code all together
root = Tk()
root.title('Test Gui')

w = 300 # open login window on center of screen ---
h = 125
# The screen info can be retrieved from the root application.
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y)) # --- end

# Create the login frame
l = LoginFrame(root)
# Pack the login frame to add it to the application
l.pack()
# Create the main frame but do not pack it, we will pack it after successful login
m = MainFrame(root) 
# Start the program running
root.mainloop()
