from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

#List of items available to hire
party_items = ["Bouncy Castle", "Tables", "Chairs", "Plates & Bowls", "Wearables", "Lights", "Sound System", "Photo Booth", "Dance Floor"]

#Instructions pop window
def show_instructions():
    messagebox.showinfo("Instructions", f'''For each item hired, Enter:

-Your Full name
-The item you are hiring
-The amount of items
                        
 Available items to hire:
{'\n'.join(party_items)}                      
''')

#validates and submit the hire program
def Submit():
    name = name_entry.get().strip()
    item_hired = item_hired_entry.get().strip().title()

    if name == "":
        messagebox.showerror("Input Error", "Name cannot be blank")
        return
    elif not name.replace(" ", "").isalpha():
        messagebox.showerror("Input Error", "Name can only contain letters, no numbers or symbols")
        return
    elif len(name.split()) < 2:
        messagebox.showerror("Input Error", "Please enter your full name (first and last name)")
        return

    if item_hired == "":
        messagebox.showerror("Input Error", "Please enter an item to hire")
        return
    elif not item_hired.replace(" ", "").isalpha():
        messagebox.showerror("Input Error", "Please enter an item to hire with only letters")
        return
    elif item_hired not in party_items:
        messagebox.showerror("Input Error", f"'{item_hired}' is not available at this Party Shop. \nAvailable items: {', '.join(party_items)}")
        return
    else:
        print(name, item_hired)

#Main window setup for Gui 
root = tk.Tk()
root.title ("Party Hire App")
root.iconbitmap('../party_shop.ico')
root.geometry ("350x400")

#Title 
title_label = ttk.Label(root, text ="Party Hire Shop", font =("Contrail One", 24, "bold"))
title_label.grid(row = 0, column = 0, columnspan = 2, pady = 20)

#Name input 
ttk.Label(root, text = "Full Name: ").grid(row = 2, column = 0, sticky = "e")
name_entry = ttk.Entry(root, width  = 25)
name_entry.grid(row = 2, column = 1)

#Item hiring input 
ttk.Label(root, text = "Item Hiring: ").grid(row = 3, column = 0, sticky = "e")
item_hired_entry = ttk.Entry(root, width  = 25)
item_hired_entry.grid(row = 3, column = 1)


#Quantity input
ttk.Label(root, text = "Number of Items: ").grid(row = 4, column = 0, sticky = "e")
quantity_item_entry = ttk.Entry(root, width  = 25)
quantity_item_entry.grid(row = 4, column = 1)

#buttons
submit_btn = ttk.Button(root, text = "Submit", command = Submit)
submit_btn.grid(row = 5, column = 0)
exit_btn = ttk.Button(root, text = "Exit", command = root.quit)#Window Exit 
exit_btn.grid(row=5, column = 1, pady = 10)
instruction_btn = ttk.Button(root, text = "Instructions", command = show_instructions)
instruction_btn.grid(row = 1, column = 3)

root.mainloop()