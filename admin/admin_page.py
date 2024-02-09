import flet as ft
from colors import *
from db import db


def admin_page(page: ft.Page):
    def login_admin(event):
        # get the data
        db.connect()
        admins = db.select_data('users', 'status = "admin"')
        db.close_connection()

        # if we have some noneeded Containers
        while len(page.views[-1].controls) > 4:
            page.views[-1].controls.pop()

        username = page.views[-1].controls[1].controls[0].content.value
        passwd = page.views[-1].controls[2].controls[0].content.value
        for admin in admins:
            if admin[2] == username and str(admin[3]) == passwd:
                page.session.set('login_admin', username)
                page.go('/admin_panel')
                return
        else:
            page.views[-1].controls.append(
                ft.Row(controls=[
                    ft.Text(
                        value='Некорректные данные!',
                        color='white',
                        bgcolor='red',
                    )
                ])
            )
            page.update()

    def create_admin(event):
        username = page.views[-1].controls[1].controls[0].content.value
        passwd = page.views[-1].controls[2].controls[0].content.value
        if not username or not passwd:
            page.views[-1].controls.append(
                ft.Row(controls=[
                    ft.Text(
                        value='Некорректные данные!',
                        color='white',
                        bgcolor='red',
                    )
                ])
            )
            page.update()
            return

        while len(page.views[-1].controls) > 4:
            page.views[-1].controls.pop()

        db.connect()
        ans = db.insert_data('users', ['admin', username, passwd, -1, "None"],
                             columns=['status', 'username', 'passwd', 'shoots', 'prizes'])
        db.close_connection()

        # get the handsome ans on the page
        if ans:
            page.views[-1].controls.append(
                ft.Row(controls=[
                    ft.Text(
                        value='Админ успешно добавлен!',
                        color='white',
                        bgcolor='green',
                    )
                ])
            )
            page.update()

    page.views.clear()  # clear all
    page.views.append(
        ft.View(controls=[

            # h1
            ft.Row(controls=[
                ft.Container(
                    ft.Text(
                        value='Вы на странице администратора',
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
                        label='Введите админский ник',
                        border_radius=15, border_width=2, border_color=PINK,
                        text_size=24, color='white', helper_text='Если нет акк-а то это ну все)'
                    ),
                    bgcolor=FWG, height=110, width=500, alignment=ft.alignment.center, padding=15,
                    border_radius=10,
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(controls=[
                ft.Container(
                    content=ft.TextField(
                        label='Введите пароль от админки',
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
                        text='Создать нового администратора',
                        icon=ft.icons.ADD_BOX,
                        on_click=create_admin,
                    ),
                    ft.FilledButton(
                        text='Войти в админ. панель',
                        icon=ft.icons.STRAIGHT,
                        on_click=login_admin,
                    )
                ])
            ], alignment=ft.MainAxisAlignment.CENTER)

        ], bgcolor=BG, horizontal_alignment=ft.alignment.center)
    )
    page.update()
