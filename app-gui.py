import tkinter as tk
from tkinter.font import Font
from boot import *

# ### 1. Creating and configuring main window
root = tk.Tk()
root.title('E-shop')
# Finding center of current screen and calculating offset
width = root.winfo_width()
height = root.winfo_height()
width = width / 2
height = height / 2
width = int(width - 200)
height = int(height - 200)
# Set window size and offset
root.geometry(f'800x600{width}{height}')

# Creating salutation frame
hello_frame = tk.Frame()
hello_frame.pack()

# Creating salutation title label
hello = tk.Label(hello_frame, text='Hello!', fg='green', font=Font(size=150))
hello.pack()

# Creating salutation subtitle label
sub_hello = tk.Label(hello_frame, text='Before starting please enter some information about you')
sub_hello.config(fg='green', font=Font(size=13))
sub_hello.pack()

# Creating frame for customer data inputs
data_frame = tk.Frame()
data_frame.pack(pady=50)

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
address_frame.pack()
address = tk.Entry(address_frame)
address.pack()

# Creating verify button
verify = tk.Button(data_frame, text='Get started!', width=10)
verify.pack(pady=20)

# Starting app
root.mainloop()
