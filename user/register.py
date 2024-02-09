import flet as ft
from colors import *
from db import db


def register(page: ft.Page):
    def register_user(event):
        username = page.views[-1].controls[1].controls[0].content.value
        passwd = page.views[-1].controls[2].controls[0].content.value
        if not username or not passwd:
            return
        db.connect()
        ans = db.insert_data('users', ['user', username, passwd, 2, ""], ['status', 'username', 'passwd', 'shoots', 'prizes'])
        db.close_connection()
        if ans:
            page.go('dashboard')
            return

    page.views.clear()
    page.views.append(
        ft.View(controls=[

            # h1
            ft.Row(controls=[
                ft.Container(
                    ft.Text(
                        value='Зарегистрироваться? По адресу!',
                        font_family='Serif',
                        size=52,
                        color='White'
                    ),
                    margin=10, padding=10, border_radius=10, bgcolor=FWG,
                    blur=ft.Blur(10, 0, ft.BlurTileMode.MIRROR),
                    border=ft.border.only(left=ft.border.BorderSide(10, PINK))
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),

            # form
            ft.Row(controls=[
                ft.Container(
                    content=ft.TextField(
                        label='Введите ник',
                        border_radius=15, border_width=2, border_color=PINK,
                        text_size=24, color='white', helper_text='Просто все, что угодно!'
                    ),
                    bgcolor=FWG, height=110, width=500, alignment=ft.alignment.center, padding=15,
                    border_radius=10,
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(controls=[
                ft.Container(
                    content=ft.TextField(
                        label='Введите ваш пароль',
                        border_radius=15, border_width=2, border_color=PINK,
                        text_size=24, color='white', password=True,
                    ),
                    bgcolor=FWG, height=100, width=500, alignment=ft.alignment.center, padding=15,
                    border_radius=10,
                )
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row(controls=[
                ft.Column(controls=[
                    ft.FilledButton(
                        text='Зарегистрироваться',
                        icon=ft.icons.ADD_BOX,
                        on_click=register_user,
                    ),
                ])
            ], alignment=ft.MainAxisAlignment.CENTER)

        ], bgcolor=BG)
    )
