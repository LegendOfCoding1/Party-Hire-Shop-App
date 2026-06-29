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
    
    quantity = quantity_items(quantity_item_entry.get())
    if quantity is None:
        return 
    print(f"Name: {name} | Item: {item_hired} | Quantity: {quantity} ")

    receipt = create_receipt_number()
    last_receipt.set(receipt)
    save_order(name, item_hired, quantity, receipt)




#Function that valiadtes the quantity of items 
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
    
#Function that creates a receipt number when order is submitted by the customer 
def create_receipt_number():
    while True:
        receipt = ""
        for i in range(RECEIPT_LENGTH):
            receipt += str(random.randint(0, 9))
        if receipt not in used_receipts:
            used_receipts.append(receipt)
            return receipt
        
#function that stores the order details 
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
def find_order(receipt):
    try:
        with open("hired_order_records.txt", "r")as file:
            for line in file:
                if receipt in line:
                    return line.strip()
    except FileNotFoundError:
        return None
    return None

def return_item():
    receipt = receipt_number_entry.get().strip()
    quantity_returned = quantity_item_returned_entry.get().strip()

    if receipt == "":
        messagebox.showerror("Input Error", "Please enter a receipt number")
        return
    
    elif  not receipt.isdigit():
        messagebox.showerror("Input Error", f"Receipt number must only contain number")
        return
    elif len(receipt) != RECEIPT_LENGTH or not receipt.isdigit():
        messagebox.showerror("Input Error", f"Receipt '{receipt}' not found")
        return 

    if quantity_returned == "":
        messagebox.showerror("Input Error", "Please enter the number of items returning")
        return
    
    try:
        quantity_returned = int(quantity_returned)
    except ValueError:
        messagebox.showerror("Input Error", "Number of Items returned must be a whole number")
        return
    
    original_order = find_order(receipt)
    if original_order is None:
        messagebox.showerror("Error", "Could not find original order details")
        return
    
    try:
        parts = original_order.split("|")
        item_name = parts[2].replace("Item:", "").strip()
        original_quantity = int(parts[3].replace("Quantity: ", "").strip().split()[0])
    except Exception:
        messagebox.showerror("Error", "Could not read original order details")
        return
    
    items_left = original_quantity - quantity_returned
    save_return(receipt, item_name, quantity_returned, original_quantity, items_left)
    
    if items_left == 0:
        remove_from_file(receipt)
        used_receipts.remove(receipt)
        messagebox.showinfo("Return Successful", f"Thank you!\n\nReceipt: {receipt}\nItem: {item_name}\nAll {original_quantity} items have been returned")
    else:
        messagebox.showinfo("Return Successful", f"Thank you!\n\nReceipt: {receipt}\nItem: {item_name}\nItems Returned: {quantity_returned}\nItems Left: {items_left} to be returned")

    receipt_number_entry.delete(0, END)
    quantity_item_returned_entry.delete(0, END)

# Saves the receipt number to clipboard and pastes into return field
def save_receipt():
    receipt = last_receipt.get()
    if receipt == "":
        messagebox.showerror("Error", "No receipt to save, please submit an order first")
        return
    receipt_number_entry.delete(0, END)
    receipt_number_entry.insert(0, receipt)
    messagebox.showinfo("Receipt Saved", f"Receipt {receipt} has been copied to the return field")
def save_return(receipt, item_name, quantity_returned, original_quantity, items_left):
    try:
        try: 
            with open("return_records.txt", "r") as file:
                contents = file.read()
        except FileNotFoundError:
            contents = ""

        with open("return_records.txt", "a")as file:
            if contents == "":
                file.write("=================================================================================""\n")
                file.write("              PARTY HIRE SHOP - RETURN RECORDS\n")
                file.write("=================================================================================""\n")
                file.write(f"{"Receipt":<20} | {"Item":<15} | {"Returned":<10} | {"Original":<10} | {"Left":<10}\n")
                file.write("---------------------------------------------------------------------------------""\n")
            file.write(f"{receipt:<20} | {item_name:<15} | {quantity_returned:<10} | {original_quantity:<10} | {items_left:<10}\n")
    except Exception as e:
        messagebox.showerror("File Error", f"Could not save return to file: {e}" )

def load_existing_receipts():
    try:
        with open("hired_order_records.txt", "r") as file:
            for line in file:
                parts = line.split("|")
                if len(parts) >=4:
                       receipt = parts[0].strip()
                       if receipt.isdigit() and len(receipt) == RECEIPT_LENGTH:
                           used_receipts.append(receipt)

    except FileNotFoundError:
        pass
def remove_from_file(receipt):
    try:
        with open("hired_order_records.txt", "r") as file:
            lines = file.readlines()

        with open("hired_order_records.txt", "w") as file:
            for line in lines:
                if receipt not in line:
                    file.write(line)
    except Exception as e:
        messagebox.showerror("File Error", f"Could not update hired items file: {e}")
        

#Main window setup for Gui 
root = tk.Tk()
root.title ("Party Hire App")
root.iconbitmap('../party_shop.ico')
root.geometry ("400x400")

last_receipt = tk.StringVar()
load_existing_receipts()
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
return_btn = ttk.Button(root, text= "Returned Item", command = return_item)
return_btn.grid(row = 10, column = 0, columnspan = 2, pady = 10)
save_receipt_btn = ttk.Button(root, text = "Save Receipt", command = save_receipt)
save_receipt_btn.grid(row=5, column = 3, padx = 5)

title_label = ttk.Label(root, text ="Returning Items", font =("Contrail One", 24, "bold"))
title_label.grid(row = 7, column = 0, columnspan = 2, pady = 20)

ttk.Label(root, text = "Receipt Number: ").grid(row = 8, column = 0, sticky = "e")
receipt_number_entry = ttk.Entry(root, width  = 25)
receipt_number_entry.grid(row = 8, column = 1)

ttk.Label(root, text = "Number of Items Returned: ").grid(row = 9, column = 0, sticky = "e")
quantity_item_returned_entry = ttk.Entry(root, width = 25)
quantity_item_returned_entry.grid(row = 9, column = 1)

root.mainloop()