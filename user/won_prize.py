import flet as ft
from colors import *
from db import db


def won_prize(page: ft.Page):
    if page.session.contains_key('login'):
        prize_id = page.session.split('/')[-1]
        db.connect()
        prize_data = db.select_data('prizes', f'id={prize_id}')
        db.close_connection()

        page.views.clear()
        page.views.append(
            ft.View(controls=[

                ft.Row(controls=[
                    ft.Text(
                        value='Поздравляем! Вы выиграли приз! Ваш приз:',
                        size=36
                    ),
                ]),

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

                ], horizontal_alignment=ft.alignment.center, vertical_alignment=ft.alignment.center)
            ]))

    else:
        page.go('/')
