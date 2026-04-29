import flet as ft
from db import *


def main(page: ft.Page):
    page.title = "🏠 Real Estate System"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO


    output = ft.Text(color="blue", size=14)


    content = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)


    def change_view(view):
        content.controls.clear()
        content.controls.append(view)
        page.update()


    
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Details")),
        ],
        rows=[]
    )


    def update_table(data):
        table.rows.clear()


        for row in data:
            table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(row[0]))),
                    ft.DataCell(ft.Text(" | ".join(map(str, row[1:])))),
                ])
            )
        page.update()


    
    title = ft.TextField(label="Title")
    address = ft.TextField(label="Address")
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


    def save_property(e):
        try:
            if not title.value or not address.value:
                output.value = "❌ Please fill all required fields"
                output.update()
                return


            price_val = float(price.value)


            add_property(title.value, address.value, "", price_val, status.value, "")
            output.value = "✅ Property added successfully"
            output.update()
            refresh()


        except ValueError:
            output.value = "❌ Please enter a valid number for price"
            output.update()
        except:
            output.value = "❌ Unexpected error"
            output.update()


    def properties_view():
        return ft.Column([
            ft.Text("🏠 Properties", size=22, weight="bold"),
            title, address, price, status,
            ft.Row([
                ft.ElevatedButton("Add Property", on_click=save_property),
                ft.ElevatedButton("Show Properties", on_click=lambda e: update_table(get_properties())),
            ]),
            table
        ])


    
    name = ft.TextField(label="Name")
    phone = ft.TextField(label="Phone", keyboard_type=ft.KeyboardType.NUMBER)


    def save_client(e):
        if not phone.value.isdigit():
            output.value = "❌ Please enter numbers only for phone"
            output.update()
            return


        add_client(name.value, phone.value, "")
        output.value = "✅ Client added successfully"
        output.update()
        refresh()


    def clients_view():
        return ft.Column([
            ft.Text("👤 Clients", size=22, weight="bold"),
            name, phone,
            ft.Row([
                ft.ElevatedButton("Add Client", on_click=save_client),
                ft.ElevatedButton("Show Clients", on_click=lambda e: update_table(get_clients())),
            ]),
            table
        ])


    
    prop_dd = ft.Dropdown(label="Property")
    client_dd = ft.Dropdown(label="Client")
    amount = ft.TextField(label="Amount")


    t_type = ft.Dropdown(
        label="Type",
        options=[
            ft.dropdown.Option("sale"),
            ft.dropdown.Option("rent"),
        ]
    )


    def refresh(e=None):
        props = get_properties()
        clients = get_clients()


        prop_dd.options = [
            ft.dropdown.Option(str(p[0]), f"{p[1]} (${p[4]})")
            for p in props
        ]


        client_dd.options = [
            ft.dropdown.Option(str(c[0]), c[1])
            for c in clients
        ]


        output.value = f"🔄 Lists updated ({len(props)} properties, {len(clients)} clients)"
        output.update()


        page.update()


    def save_transaction(e):
        if not prop_dd.value or not client_dd.value:
            output.value = "❌ Please select property and client"
            output.update()
            return


        try:
            amount_val = float(amount.value)


            create_transaction(
                int(prop_dd.value),
                int(client_dd.value),
                t_type.value,
                amount_val,
                "2026-01-01"
            )


            output.value = "✅ Transaction completed successfully"
            output.update()
            refresh()


        except ValueError:
            output.value = "❌ Please enter a valid number for amount"
            output.update()
        except Exception as err:
            output.value = f"❌ {err}"
            output.update()


    def transactions_view():
        return ft.Column([
            ft.Text("💰 Transactions", size=22, weight="bold"),
            prop_dd, client_dd, amount, t_type,
            ft.Row([
                ft.ElevatedButton("Refresh Lists", on_click=refresh),
                ft.ElevatedButton("Create Transaction", on_click=save_transaction),
                ft.ElevatedButton("Show Transactions", on_click=lambda e: update_table(get_transactions())),
            ]),
            table
        ])


    
    def dashboard_view():
        def show(e):
            stats = get_dashboard_stats()
            output.value = (
                f"Total: {stats['total_properties']} | "
                f"Available: {stats['available']} | "
                f"Sold: {stats['sold']} | "
                f"Rented: {stats['rented']} | "
                f"Clients: {stats['clients']}"
            )
            output.update()


        return ft.Column([
            ft.Text("📊 Dashboard", size=22, weight="bold"),
            ft.ElevatedButton("Show Statistics", on_click=show)
        ])


    
    def reports_view():
        return ft.Column([
            ft.Text("📄 Reports", size=22, weight="bold"),
            ft.ElevatedButton("Show Available Properties", on_click=lambda e: update_table(get_available_properties())),
            table
        ])


    
    menu = ft.Row([
        ft.ElevatedButton("Dashboard", on_click=lambda e: change_view(dashboard_view())),
        ft.ElevatedButton("Properties", on_click=lambda e: change_view(properties_view())),
        ft.ElevatedButton("Clients", on_click=lambda e: change_view(clients_view())),
        ft.ElevatedButton("Transactions", on_click=lambda e: change_view(transactions_view())),
        ft.ElevatedButton("Reports", on_click=lambda e: change_view(reports_view())),
    ])


    page.add(
        ft.Text("🏠 Real Estate System", size=28, weight="bold"),
        menu,
        ft.Divider(),
        content,
        ft.Divider(),
        ft.Text("System Messages:", weight="bold"),
        output
    )


    change_view(dashboard_view())
    refresh()


ft.app(target=main)
