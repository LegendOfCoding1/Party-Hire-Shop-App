from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

#Main window setup for Gui 
root = tk.Tk()
root.title ("Party Hire Shop")
root.iconbitmap('../party_shop.ico')
root.geometry ("350x350")

#Title 
title_label = ttk.Label(root, text ="Party Hire Shop", font =("Contrail One", 24, "bold"))
title_label.grid(row = 0, column = 0, columnspan = 2, pady = 20)

#Name input 
ttk.Label(root, text = "Name: ").grid(row = 1, column = 0, sticky = "e")
name_entry = ttk.Entry(root, width  = 25)
name_entry.grid(row = 1, column = 1)

#Item hiring input 
ttk.Label(root, text = "Item Hiring: ").grid(row = 2, column = 0, sticky = "e")
item_hired = ttk.Entry(root, width  = 25)
item_hired.grid(row = 2, column = 1)

#Quantity input
ttk.Label(root, text = "Number of Items: ").grid(row = 3, column = 0, sticky = "e")
quantity_item = ttk.Entry(root, width  = 25)
quantity_item.grid(row = 3, column = 1)

#buttons
submit_btn = ttk.Button(root, text = "Submit")
submit_btn.grid(row = 5, column = 0)
exit_btn = ttk.Button(root, text = "Exit", command = root.quit)#Window Exit 
exit_btn.grid(row=5, column = 1, pady = 10)

root.mainloop()