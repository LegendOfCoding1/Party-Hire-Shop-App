from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import random

#Constants
MIN_ITEMS = 1
MAX_ITEMS = 500
RECEIPT_LENGTH = 12

#Stores used receipt numbers so they never can repeated 
used_receipts = []
#List of items available to hire
party_items = ["Bouncy Castle", "Tables", "Chairs", "Plates and Bowls", "Wearables", "Lights", "Sound System", "Photo Booth", "Dance Floor"]

def show_instructions():
    items_list = "\n".join(party_items)
    messagebox.showinfo("Instructions", f"""For each item hired, Enter:
                        
-Your Full Name
-The item you are hiring
-The amount of items

Available items to hire:
{items_list}
""")


#validates and submit the hire program
def Submit():
    name = name_entry.get().strip().title()
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
    elif len(name) > 50:
        messagebox.showerror("Input Error", "Name cannot be 50 characters long.")

    if item_hired == "":
        messagebox.showerror("Input Error", "Please enter an item to hire")
        return
    elif not item_hired.replace(" ", "").isalpha():
        messagebox.showerror("Input Error", "Please enter an item to hire with only letters")
        return
    elif item_hired not in party_items:
        messagebox.showerror("Input Error", f"'{item_hired}' is not available at this Party Shop. \nAvailable items: {', '.join(party_items)}")
        return
    
    quantity = quantity_items(quantity_item_entry.get())
    if quantity is None:
        return 
    print(f"Name: {name} | Item: {item_hired} | Quantity: {quantity} ")

    receipt = create_receipt_number()
    save_order(name, item_hired, quantity, receipt)

def quantity_items(quantity):
    quantity = quantity.strip()
    
    if quantity == "":
        messagebox.showerror("Input Error", "Number of items cannot be blank")
        return None

    try: 
        quantity = int(quantity)
        if quantity < MIN_ITEMS or quantity > MAX_ITEMS:
            messagebox.showerror("Input Error", f'Number of items must be between {MIN_ITEMS} and {MAX_ITEMS}')
            return None
        return quantity
    except ValueError:
        messagebox.showerror("Input Error", "Number of items must be whole numbers, no letter or symbols ")
        return None
    
  
def create_receipt_number():
    while True:
        receipt = ""
        for i in range(RECEIPT_LENGTH):
            receipt += str(random.randint(0, 9))
        if receipt not in used_receipts:
            used_receipts.append(receipt)
            return receipt

def save_order(name, item, quantity, receipt):
    try:
        try:
            with open("hired_order_records.txt", "r") as file:
                contents = file.read()
        except FileNotFoundError:
            contents = ""
        
        with open("hired_order_records.txt", "a") as file:
            if contents == "":
                file.write("=================================================================================""\n")
                file.write("              PARTY HIRE SHOP - ORDER RECORDS\n")
                file.write("=================================================================================""\n")
                file.write(f"{'Receipt':<20} | {'Name':<15} | {'Item':<15} | {'Quantity'} |\n")
                file.write("---------------------------------------------------------------------------------""\n")
            file.write(f"{receipt:<20} | {name:<15} | {item:<15} | {quantity}        |\n")
        messagebox.showinfo("Success", f"Order saved successfully!\n\nReceipt Number: {receipt}\nName: {name}\nItem: {item}\nQuantity: {quantity}")

    except Exception as e:
        messagebox.showerror("File Error", f"Could not save order to file: {e}")






        
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