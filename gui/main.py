from behavior import *

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
root.geometry(f'1024x576{width}{height}')

# Creating salutation text
hello = tk.Label(text='Hello! Please enter all data to start.', font='Arial 30')
hello.config(bd=50)
hello.pack()

# Creating input field for customer first name
fn_label = tk.Label(text='Your name', font='Sans 10')
fn_label.pack()
fn_entry = tk.Entry(width=12)
fn_entry.pack()

# Starting app
root.mainloop()
