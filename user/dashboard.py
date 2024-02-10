import flet as ft
from colors import *


def dashboard(page: ft.Page):
    def logout_user(event):
        page.session.remove('login')
        page.go('/')
        return

    if page.session.contains_key('login'):
        username = page.session.get('login')

        page.views.clear()
        page.views.append(
            ft.View(controls=[

                ft.Row(controls=[
                    ft.Column(controls=[
                        ft.ElevatedButton(
                            text='Выйти из аккаунта',
                            icon=ft.icons.EXIT_TO_APP,
                            icon_color='red200',
                            on_click=logout_user
                        )
                    ])
                ])

            ], horizontal_alignment=ft.alignment.center, bgcolor=BG)
        )
        page.update()

        # TODO: сделать саму логику игры
    else:
        page.go('/')
