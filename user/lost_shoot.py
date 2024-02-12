import flet as ft
from colors import *


def lost_shoot(page: ft.Page):
    if page.session.contains_key('login'):

        page.views.clear()
        page.views.append(
            ft.View(controls=[
                ft.Text(
                    value='Увы, тут ничего нет((('
                )
            ], horizontal_alignment=ft.alignment.center, vertical_alignment=ft.alignment.center)
        )
        page.update()
    else:
        page.go('/')
