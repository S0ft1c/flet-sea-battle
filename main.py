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
        if '/add_ship' in page.route:
            admin.add_ship(page)
        if page.route == '/shoots':
            admin.shoots(page)
        if 'add_shoots' in page.route:
            admin.add_shoots_to_person(page)
        if 'remove_shoots' in page.route:
            admin.remove_shoots_from_person(page)
        if page.route == '/was_prize':
            user.was_prize(page)
        if page.route == '/lost_shoot':
            user.lost_shoot(page)
        if page.route == '/prizes_page':
            user.prizes_page(page)
        if '/won_prize' in page.route:
            user.won_prize(page)

    page.bgcolor = BG
    page.on_route_change = route_changed
    page.go(page.route)


ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=5000, upload_dir='data/uploads', assets_dir='data')
