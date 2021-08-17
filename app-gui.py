import tkinter as tk
from tkinter.font import Font
from gui.config import *
from boot import *

# ### 1. Creating and configuring main window with start screen
root = tk.Tk()
root.title('E-shop')
# Finding center of current screen and calculating offset
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
# Set window size
root.geometry(f'{width}x{height- 60}')

# Creating salutation frame
hello_frame = tk.Frame()
hello_frame.pack()

# Creating salutation title label
hello = tk.Label(hello_frame, text='Hello!', font=Font(size=150), fg='#00DD00')
hello.pack()

# Creating salutation subtitle label
sub_hello = tk.Label(hello_frame, text='Before starting please enter some information about you')
sub_hello.config(font=Font(size=13), fg='gray38')
sub_hello.pack()

# Creating frame for customer data inputs
data_frame = tk.Frame()
data_frame.pack(pady=30)

# Creating frame with customer first name input field
name_frame = tk.LabelFrame(data_frame, text='First name')
name_frame.pack(ipadx=5, ipady=3)
name = tk.Entry(name_frame)
name.pack()

# Creating frame with customer last name input field
surname_frame = tk.LabelFrame(data_frame, text='Last name')
surname_frame.pack(ipadx=5, ipady=3)
surname = tk.Entry(surname_frame)
surname.pack()

# Creating frame with customer address name input field
address_frame = tk.LabelFrame(data_frame, text='Address')
address_frame.pack(ipadx=5, ipady=3)
tk.Label(address_frame, text='Country', font=Font(size=9)).pack()
country = tk.Entry(address_frame)
country.pack()
tk.Label(address_frame, text='City').pack()
city = tk.Entry(address_frame)
city.pack()
tk.Label(address_frame, text='Street').pack()
street = tk.Entry(address_frame)
street.pack()
tk.Label(address_frame, text='Street number').pack()
number = tk.Entry(address_frame)
number.pack()

# Creating verify and start app button logic
error = None
def verify_and_start():
    global error
    global activeUser
    # verify address data
    try:
        address = Address(country.get(), city.get(), street.get(), number.get())
        correct = True
    except NameError as n:
        if error != None:
            error.destroy()
        if str(n) == 'value cannot be an empty string':
            error = tk.Label(data_frame,
             text='Error: country, city or/and street field(s) is empty!')
        elif str(n) == 'the value contains only the same letters':
            error = tk.Label(data_frame,
             text='Error: country, city or/and street contain(s) only the same letters!')
        elif str(n) == 'the value must not contains integer values':
            error = tk.Label(data_frame,
             text='Error: country, city or/and street contain(s) numbers!')
        error.pack()
        correct = False
    except ValueError as v:
        if error != None:
            error.destroy()
        if str(v) == 'value must not be empty':
            error = tk.Label(data_frame,
             text='Error: street number field is empty or not contains number(s)!')
        elif str(v) == 'value contains only the same characters':
            error = tk.Label(data_frame,
             text='Error: street number contains only the same characters')
        elif str(v) == 'value must not contains letters':
            error = tk.Label(data_frame,
             text='Error: street number contains letters!')
        error.pack()
        correct = False
    # verify customer data
    if correct:
        try:
            user = Customer(name.get(), surname.get(), address)
            activeUser = user
            finish = True
        except NameError as n:
            if error != None:
                error.destroy()
            if str(n) == 'name cannot be an empty string':
                error = tk.Label(
                    data_frame,
                     text='Error: first name or/and last name field(s) is empty!')
            elif str(n) == 'the name contains only the same letters':
                error = tk.Label(
                    data_frame,
                     text='Error: first name or/and last name contain(s) only the same letters!')
            elif str(n) == 'the name must not contain integer values':
                error = tk.Label(
                    data_frame,
                     text='Error: first name or/and last name contain(s) numbers!')
            error.pack()
            finish = False
        # starting app if all data is correct
        if finish:
            start_app()

# Creating verify and start app button
verify = tk.Button(data_frame, text='Get started!', width=10, command=verify_and_start)
verify.pack(pady=20, ipadx=5, ipady=3)


# ### 2. Creating shop screen
def start_app():
    # Preparing window
    hello_frame.destroy()
    data_frame.destroy()
    root.config(bg='white')

    # Creating main menu frame
    main_menu = tk.Frame(root, bg='gray80')
    main_menu.pack(side='left', fill='y', ipadx=60)


# Starting app
root.mainloop()
