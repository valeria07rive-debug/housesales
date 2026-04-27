import flet as ft
from db import add_property, get_properties, add_client, get_clients


def main(page: ft.Page):
    page.title = "Real Estate System"
    page.scroll = "auto"

   
    title = ft.TextField(label="Title")
    address = ft.TextField(label="Address")
    ptype = ft.TextField(label="Type")
    price = ft.TextField(label="Price")
    status = ft.TextField(label="Status")
    desc = ft.TextField(label="Description")

    output = ft.Text("")  

   
    def save_property(e):
        if title.value == "" or price.value == "":
            output.value = "❌ Title and Price are required"
            page.update()
            return

        try:
            price_value = float(price.value)  
        except:
            output.value = "❌ Price must be a number"
            page.update()
            return

        try:
            add_property(
                title.value,
                address.value,
                ptype.value,
                price_value,
                status.value,
                desc.value
            )
            output.value = "✅ Property added"
        except Exception as err:
            output.value = f"❌ Error: {err}"

        page.update()

    
    def show_properties(e):
        props = get_properties()
        output.value = f"PROPERTIES:\n{props}"
        page.update()

   
    name = ft.TextField(label="Name")
    phone = ft.TextField(label="Phone")
    email = ft.TextField(label="Email")

    
    def save_client(e):
        if name.value == "":
            output.value = "❌ Name is required"
            page.update()
            return

        try:
            add_client(name.value, phone.value, email.value)
            output.value = "✅ Client added"
        except Exception as err:
            output.value = f"❌ Error: {err}"

        page.update()

    
    def show_clients(e):
        clients = get_clients()
        output.value = f"CLIENTS:\n{clients}"
        page.update()

    
    page.add(
        ft.Text("🏠 REAL ESTATE SYSTEM", size=20),

        ft.Text("--- ADD PROPERTY ---"),
        title, address, ptype, price, status, desc,
        ft.ElevatedButton("Add Property", on_click=save_property),
        ft.ElevatedButton("Show Properties", on_click=show_properties),

        ft.Divider(),

        ft.Text("--- ADD CLIENT ---"),
        name, phone, email,
        ft.ElevatedButton("Add Client", on_click=save_client),
        ft.ElevatedButton("Show Clients", on_click=show_clients),

        ft.Divider(),

        ft.Text("OUTPUT:"),
        output
    )


ft.app(target=main)
