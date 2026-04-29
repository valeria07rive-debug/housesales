import flet as ft
from db import *


def main(page: ft.Page):
    page.title = "🏠 Real Estate System"
    page.padding = 20


    output = ft.Text(color="blue")
    content = ft.Column()


    # ================= VIEW SWITCH =================
    def change_view(view):
        content.controls.clear()
        content.controls.append(view)
        page.update()


    # ================= TABLE =================
    table = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Info")),
        ft.DataColumn(ft.Text("Actions")),
    ])


    def update_table(data):
        table.rows = []
        for row in data:
            pid = row[0]


            table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(pid))),
                    ft.DataCell(ft.Text(str(row))),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton("delete", on_click=lambda e, id=pid: delete_item(id)),
                            ft.IconButton("edit", on_click=lambda e, id=pid: load_edit(id)),
                        ])
                    )
                ])
            )
        page.update()


    # ================= DELETE =================
    def delete_item(pid):
        delete_property(pid)
        output.value = f"Deleted {pid}"
        page.update()


    # ================= EDIT =================
    edit_id = ft.TextField(label="ID", disabled=True)
    edit_title = ft.TextField(label="Title")
    edit_address = ft.TextField(label="Address")
    edit_price = ft.TextField(label="Price")
    edit_status = ft.Dropdown(options=[
        ft.dropdown.Option("available"),
        ft.dropdown.Option("sold"),
        ft.dropdown.Option("rented"),
        ft.dropdown.Option("reserved"),
    ])


    def load_edit(pid):
        props = get_properties()
        for p in props:
            if p[0] == pid:
                edit_id.value = str(p[0])
                edit_title.value = p[1]
                edit_address.value = p[2]
                edit_price.value = str(p[4])
                edit_status.value = p[5]
        page.update()


    def save_edit(e):
        update_property(
            int(edit_id.value),
            edit_title.value,
            edit_address.value,
            float(edit_price.value),
            edit_status.value
        )
        output.value = "Updated!"
        page.update()


    edit_section = ft.Column([
        ft.Text("Edit Property", size=16),
        edit_id, edit_title, edit_address, edit_price, edit_status,
        ft.ElevatedButton("Save Changes", on_click=save_edit)
    ])


    # ================= PROPERTIES =================
    title = ft.TextField(label="Title")
    address = ft.TextField(label="Address")
    price = ft.TextField(label="Price")


    status = ft.Dropdown(options=[
        ft.dropdown.Option("available"),
        ft.dropdown.Option("sold"),
        ft.dropdown.Option("rented"),
        ft.dropdown.Option("reserved"),
    ])


    filter_status = ft.Dropdown(
        label="Filter",
        options=[
            ft.dropdown.Option("all"),
            ft.dropdown.Option("available"),
            ft.dropdown.Option("sold"),
            ft.dropdown.Option("rented"),
        ]
    )


    def save_property(e):
        add_property(title.value, address.value, "", float(price.value), status.value, "")
        output.value = "Added!"
        page.update()


    def show_filtered(e):
        data = get_properties()
        if filter_status.value and filter_status.value != "all":
            data = [d for d in data if d[5] == filter_status.value]
        update_table(data)


    def properties_view():
        return ft.Column([
            ft.Text("Properties", size=20),
            title, address, price, status,
            ft.Row([
                ft.ElevatedButton("Add", on_click=save_property),
                ft.ElevatedButton("Show", on_click=show_filtered),
            ]),
            filter_status,
            table,
            edit_section
        ])


    # ================= CLIENTS =================
    name = ft.TextField(label="Name")
    phone = ft.TextField(label="Phone")


    def save_client(e):
        add_client(name.value, phone.value, "")
        output.value = "Client added"
        page.update()


    def clients_view():
        return ft.Column([
            ft.Text("Clients", size=20),
            name, phone,
            ft.ElevatedButton("Add", on_click=save_client),
            ft.ElevatedButton("Show", on_click=lambda e: update_table(get_clients())),
            table
        ])


    # ================= TRANSACTIONS =================
    prop_dd = ft.Dropdown(label="Property")
    client_dd = ft.Dropdown(label="Client")


    def refresh(e=None):
        prop_dd.options = [ft.dropdown.Option(str(p[0]), p[1]) for p in get_properties()]
        client_dd.options = [ft.dropdown.Option(str(c[0]), c[1]) for c in get_clients()]
        page.update()


    def save_transaction(e):
        create_transaction(int(prop_dd.value), int(client_dd.value), "sale", 1000, "2026")
        output.value = "Transaction done"
        page.update()


    def transactions_view():
        return ft.Column([
            ft.Text("Transactions", size=20),
            prop_dd, client_dd,
            ft.Row([
                ft.ElevatedButton("Refresh", on_click=refresh),
                ft.ElevatedButton("Create", on_click=save_transaction),
                ft.ElevatedButton("Show", on_click=lambda e: update_table(get_transactions())),
            ]),
            table
        ])


    # ================= DASHBOARD =================
    def dashboard_view():
        return ft.Column([
            ft.Text("Dashboard", size=20),
            ft.ElevatedButton("Show Stats", on_click=lambda e: output.__setattr__("value", str(get_dashboard_stats())))
        ])


    # ================= REPORTS =================
    def reports_view():
        return ft.Column([
            ft.Text("Reports", size=20),
            ft.ElevatedButton("Available", on_click=lambda e: update_table(get_available_properties())),
            table
        ])


    # ================= MENU =================
    menu = ft.Row([
        ft.ElevatedButton("Dashboard", on_click=lambda e: change_view(dashboard_view())),
        ft.ElevatedButton("Properties", on_click=lambda e: change_view(properties_view())),
        ft.ElevatedButton("Clients", on_click=lambda e: change_view(clients_view())),
        ft.ElevatedButton("Transactions", on_click=lambda e: change_view(transactions_view())),
        ft.ElevatedButton("Reports", on_click=lambda e: change_view(reports_view())),
    ])


    page.add(
        ft.Text("🏠 Real Estate System", size=26),
        menu,
        ft.Divider(),
        content,
        ft.Divider(),
        output
    )


    change_view(dashboard_view())
    refresh()


ft.app(target=main)
