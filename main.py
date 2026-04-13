import tkinter as tk
from db import add_property, get_properties, add_client, get_clients

root = tk.Tk()
root.title("Real Estate")
root.geometry("400x500")

tk.Label(root, text="--- ADD PROPERTY ---").pack()

title = tk.Entry(root)
title.pack()

address = tk.Entry(root)
address.pack()

ptype = tk.Entry(root)
ptype.pack()

price = tk.Entry(root)
price.pack()

status = tk.Entry(root)
status.pack()

desc = tk.Entry(root)
desc.pack()


def save_property():
    add_property(
        title.get(),
        address.get(),
        ptype.get(),
        float(price.get()),
        status.get(),
        desc.get()
    )
    print("Property added 😎")


tk.Button(root, text="Add Property", command=save_property).pack()


def show_properties():
    print("PROPERTIES:")
    print(get_properties())


tk.Button(root, text="Show Properties", command=show_properties).pack()

