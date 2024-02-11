import flet as ft
from colors import *
from db import db


def shoots(page: ft.Page):
    def add_shoots_to_person(event):
        id = -1
        column_flet = page.views[-1].controls[-1].controls[0]
        for el in column_flet.controls:
            if event.control == el.content.controls[-2].controls[0].content:
                id = int(el.content.controls[0].controls[0].content.value.split()[-1])
                break
        page.go(f'/add_shoots/{id}')
        return

    def remove_shoots_from_person(event):
        id = -1
        column_flet = page.views[-1].controls[-1].controls[0]
        for el in column_flet.controls:
            if event.control == el.content.controls[-1].controls[0].content:
                id = int(el.content.controls[0].controls[0].content.value.split()[-1])
                break
        page.go(f'/remove_shoots/{id}')
        return

    def get_users():
        db.connect()
        users = db.select_data('users', 'status="user"')
        db.close_connection()

        rows = []
        for user in users:
            rows.append(ft.Container(
                content=ft.Row(controls=[
                    ft.Column(controls=[ft.Container(
                        content=ft.Text(value=f'id: {user[0]}', bgcolor=FWG),
                        bgcolor='white', border_radius=15, border=ft.border.all(5, FWG)
                    )]),
                    ft.Column(controls=[ft.Container(
                        content=ft.Text(value=f'username: {user[2]}', bgcolor=FWG),
                        bgcolor='white', border_radius=15, border=ft.border.all(5, FWG)
                    )]),
                    ft.Column(controls=[ft.Container(
                        content=ft.Text(value=f'shoots: {user[4]}', bgcolor=FWG),
                        bgcolor='white', border_radius=15, border=ft.border.all(5, FWG)
                    )]),
                    ft.Column(controls=[ft.Container(
                        content=ft.IconButton(icon=ft.icons.ADD, icon_color='green', on_click=add_shoots_to_person),
                        bgcolor='white', border_radius=15, border=ft.border.all(5, FWG)
                    )]),
                    ft.Column(controls=[ft.Container(
                        content=ft.IconButton(icon=ft.icons.REMOVE, icon_color='red',
                                              on_click=remove_shoots_from_person),
                        bgcolor='white', border_radius=15, border=ft.border.all(5, FWG)
                    )]),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor='white', border=ft.border.all(5, 'blue200'), border_radius=15
            ))
        return rows

    if page.session.contains_key('login_admin'):
        page.views.clear()

        page.views.append(
            ft.View(controls=[

                ft.Row(controls=[
                    ft.Column(controls=[
                        ft.Container(
                            ft.Text(
                                value='Выберите кому добавить!',
                                font_family='Serif',
                                size=52,
                                color='White'
                            ),
                            margin=10, padding=10, border_radius=10, bgcolor=FWG,
                            blur=ft.Blur(10, 0, ft.BlurTileMode.MIRROR),
                            border=ft.border.only(left=ft.border.BorderSide(10, PINK))
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ]),

                ft.Row(controls=[
                    ft.Column(controls=[
                        ft.Container(
                            ft.Text(
                                value='Рядом с каждым пользователем есть плюс и минус.\nНа плюс добавлять выстрелы, а'
                                      ' на минус удалять',
                                font_family='Serif',
                                size=24,
                                color='White'
                            ),
                            margin=10, padding=10, border_radius=10, bgcolor=FWG,
                            blur=ft.Blur(10, 0, ft.BlurTileMode.MIRROR),
                            border=ft.border.only(left=ft.border.BorderSide(10, PINK))
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ]),

                ft.Row(controls=[
                    ft.Column(controls=get_users(), scroll=ft.ScrollMode.ALWAYS, spacing=10, width=500, height=700)
                ], alignment=ft.MainAxisAlignment.CENTER)

            ], horizontal_alignment=ft.alignment.center, bgcolor=BG)
        )
        page.update()
    else:
        page.go('/')
