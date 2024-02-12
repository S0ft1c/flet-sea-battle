import flet as ft
from colors import *
from db import db


def prizes_page(page: ft.Page):
    def get_all_prizes():
        db.connect()
        user_data = db.select_data('users', f'id={user[0]}')[0]
        db.close_connection()

        col = ft.Column(scroll=ft.ScrollMode.ALWAYS)

        if not user_data[-1]:
            col.controls.append(
                ft.Text(value='Пока тут ничего нет...')
            )
        else:
            prizes = sorted(list(set(user_data[-1].split(', '))))
            for prize in prizes:
                db.connect()
                prize_data = db.select_data('prizes', f'id={prize}')[0]
                db.close_connection()

                col.controls.append(
                    ft.Row(controls=[
                        ft.Container(
                            content=ft.Column(controls=[
                                ft.Row(controls=[
                                    ft.Text(value=prize_data[0], color='black', size=12)
                                ]),
                                ft.Row(controls=[
                                    ft.Text(value=prize_data[1], color='black', size=24)
                                ]),
                                ft.Row(controls=[
                                    ft.Text(value=prize_data[2], color='black', size=16),
                                ]),
                                ft.Row(controls=[
                                    ft.Image(src=prize_data[3], width=300, height=400)
                                ])
                            ]), bgcolor='white', border_radius=10, border=ft.border.all(8, 'purple'),
                        )
                    ])
                )
            return col

    if page.session.contains_key('login'):

        user = page.session.get('login')

        page.views.clear()
        page.views.append(
            ft.View(controls=[

                get_all_prizes(),

            ])
        )
        page.update()
    else:
        page.go('/')
