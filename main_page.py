import flet as ft
from db import db
from colors import *


def main_page(page: ft.Page):
    def go_to_admin(event):
        page.go('/admin')

    def go_to_register(event):
        page.go('/register')

    def login(event):
        username = page.views[-1].controls[3].controls[0].content.value
        passwd = page.views[-1].controls[4].controls[0].content.value

        db.connect()
        data = db.select_data('users', f'username="{username}" and passwd="{passwd}"')
        db.close_connection()

        if data:
            page.session.set('login', username)
            page.go('/dashboard')

    # check for the tokens
    if page.session.contains_key('login'):
        page.go('dashboard')
        return
    elif page.session.contains_key('login_admin'):
        page.go('/admin_panel')
        return

    page.views.clear()
    page.views.append(ft.View(controls=[
        ft.Row(controls=[
            ft.Container(
                ft.Text(
                    value='Добро пожаловать в нашу лотерею!',
                    font_family='Serif',
                    size=52,
                    color='White'
                ),
                margin=10, padding=10, border_radius=10, bgcolor=FWG,
                blur=ft.Blur(10, 0, ft.BlurTileMode.MIRROR),
                border=ft.border.only(left=ft.border.BorderSide(10, PINK))
            ),
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Row(controls=[
            ft.Container(
                ft.Text(
                    value='Здесь вы можете опробовать свою удачу в игре "Морской бой!"',
                    font_family='Serif',
                    color='white',
                    size=24,
                ),
                margin=10, padding=10, border_radius=10, bgcolor=FWG,
                blur=ft.Blur(10, 0, ft.BlurTileMode.MIRROR),
                border=ft.border.only(left=ft.border.BorderSide(10, PINK))
            ),
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Row(controls=[
            ft.Text(
                value='Но для начала неплохо было бы войти в свой аккаунт)',
                size=16,
                color='white'
            )
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Row(controls=[
            ft.Container(
                content=ft.TextField(
                    label='Введите свой ник',
                    border_radius=15, border_width=2, border_color=PINK,
                    text_size=24, color='white', helper_text='Если нет акк-а можно зарегистрироваться!'
                ),
                bgcolor=FWG, height=100, width=500, alignment=ft.alignment.center, padding=15,
                border_radius=10,
            )
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Row(controls=[
            ft.Container(
                content=ft.TextField(
                    label='Введите пароль от вашего аккаунта',
                    border_radius=15, border_width=2, border_color=PINK,
                    text_size=24, color='white', password=True
                ),
                bgcolor=FWG, height=100, width=500, alignment=ft.alignment.center, padding=15,
                border_radius=10,
            )
        ], alignment=ft.MainAxisAlignment.CENTER),

        ft.Row(controls=[
            ft.Column(controls=[
                ft.FilledButton(
                    text='Зарегистрироваться',
                    icon=ft.icons.AC_UNIT,
                    on_long_press=go_to_admin,
                    on_click=go_to_register
                )
            ]),
            ft.Column(controls=[
                ft.FilledButton(
                    text='Войти',
                    icon=ft.icons.STRAIGHT,
                    on_click=login
                )
            ]),
        ], alignment=ft.MainAxisAlignment.CENTER)

    ],
        bgcolor=BG
    ))
    page.update()
