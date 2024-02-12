import flet as ft
from colors import *


def was_prize(page: ft.Page):
    if page.session.contains_key('login'):

        page.views.clear()
        page.views.append(
            ft.View(controls=[

                ft.Text(
                    value='Вы уже получали такой приз!('
                )

            ], horizontal_alignment=ft.alignment.center, vertical_alignment=ft.alignment.center)
        )

    else:
        page.go('/')
