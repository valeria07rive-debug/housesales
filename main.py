import flet as ft
from db import add_property, get_properties, add_client, get_clients


def main(page: ft.Page):
    page.title = "Real Estate System"
    page.scroll = "auto"

    output = ft.Text("")

    
    title = ft.TextField(label="Title")
    address = ft.TextField(label="Address")
    ptype = ft.TextField(label="Type")

    price = ft.TextField(label="Price")

    status = ft.Dropdown(
        label="Status",
        options=[
            ft.dropdown.Option("available"),
            ft.dropdown.Option("sold"),
            ft.dropdown.Option("rented"),
            ft.dropdown.Option("reserved"),
        ]
    )

    desc = ft.TextField(label="Description")

    def save_property(e):
        try:
            # VALIDAR PRECIO
            price_value = float(price.value)

            if not title.value or not address.value:
                output.value = "❌ Title and Address required"
                page.update()
                return

            if not status.value:
                output.value = "❌ Select a status"
                page.update()
                return

            add_property(
                title.value,
                address.value,
                ptype.value,
                price_value,
                status.value,
                desc.value
            )

            output.value = "✅ Property added"
            page.update()

        except ValueError:
            output.value = "❌ Price must be a number"
            page.update()
        except Exception as err:
            output.value = f"❌ Error: {err}"
            page.update()

    def show_properties(e):
        try:
            props = get_properties()
            output.value = f"PROPERTIES:\n{props}"
            page.update()
        except Exception as err:
            output.value = f"❌ Error: {err}"
            page.update()

    
    name = ft.TextField(label="Name")
    phone = ft.TextField(label="Phone")
    email = ft.TextField(label="Email")

    def save_client(e):
        try:
            
            if not phone.value.isdigit():
                output.value = "❌ Phone must contain only numbers"
                page.update()
                return

            if not name.value:
                output.value = "❌ Name required"
                page.update()
                return

            add_client(name.value, phone.value, email.value)

            output.value = "✅ Client added"
            page.update()

        except Exception as err:
            output.value = f"❌ Error: {err}"
            page.update()

    def show_clients(e):
        try:
            clients = get_clients()
            output.value = f"CLIENTS:\n{clients}"
            page.update()
        except Exception as err:
            output.value = f"❌ Error: {err}"
            page.update()

    
    page.add(
        ft.Text("🏠 REAL ESTATE SYSTEM", size=20, weight="bold"),

        ft.Divider(),

        ft.Text("--- ADD PROPERTY ---"),
        title,
        address,
        ptype,
        price,
        status,
        desc,
        ft.ElevatedButton("Add Property", on_click=save_property),
        ft.ElevatedButton("Show Properties", on_click=show_properties),

        ft.Divider(),

        ft.Text("--- ADD CLIENT ---"),
        name,
        phone,
        email,
        ft.ElevatedButton("Add Client", on_click=save_client),
        ft.ElevatedButton("Show Clients", on_click=show_clients),

        ft.Divider(),

        ft.Text("OUTPUT:"),
        output
    )


ft.app(target=main)


