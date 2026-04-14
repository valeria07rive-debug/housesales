import flet as ft
from db import add_property, get_properties, add_client, get_clients

def main(page: ft.Page):
    page.title = "Real Estate"
    page.scroll = "auto"


    title = ft.TextField(label="Title")
    address = ft.TextField(label="Address")
    ptype = ft.TextField(label="Type")
    price = ft.TextField(label="Price")
    status = ft.TextField(label="Status")
    desc = ft.TextField(label="Description")

    def save_property(e):
        add_property(
            title.value,
            address.value,
            ptype.value,
            float(price.value),
            status.value,
            desc.value
        )
        page.add(ft.Text("Property added 😎"))

    def show_properties(e):
        props = get_properties()
        page.add(ft.Text(f"PROPERTIES:\n{props}"))

   
    name = ft.TextField(label="Name")
    phone = ft.TextField(label="Phone")
    email = ft.TextField(label="Email")

    def save_client(e):
        add_client(name.value, phone.value, email.value)
        page.add(ft.Text("Client added 😎"))

    def show_clients(e):
        clients = get_clients()
        page.add(ft.Text(f"CLIENTS:\n{clients}"))

   
    page.add(
        ft.Text("--- ADD PROPERTY ---"),
        title, address, ptype, price, status, desc,
        ft.ElevatedButton("Add Property", on_click=save_property),
        ft.ElevatedButton("Show Properties", on_click=show_properties),

        ft.Divider(),

        ft.Text("--- ADD CLIENT ---"),
        name, phone, email,
        ft.ElevatedButton("Add Client", on_click=save_client),
        ft.ElevatedButton("Show Clients", on_click=show_clients),
    )

ft.app(target=main)
