import flet as ft
import admin as admin
import user as user
from main_page import main_page
from colors import *


def main(page: ft.Page):
    def route_changed(route):
        if page.route == '/':
            main_page(page)
        if page.route == '/admin':
            admin.admin_page(page)
        if page.route == '/admin_panel':
            admin.admin_panel(page)
        if page.route == '/register':
            user.register(page)
        if page.route == '/dashboard':
            user.dashboard(page)
        if page.route == '/add_prize':
            admin.add_prize(page)

    page.bgcolor = BG
    page.on_route_change = route_changed
    page.go(page.route)


ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=5000, upload_dir='data/uploads', assets_dir='data')
