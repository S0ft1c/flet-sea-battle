import flet as ft
from colors import *
from db import db


def add_ship(page: ft.Page):
    if page.session.contains_key('login_admin'):
        def get_all_prizes():
            def choose_prize(event):
                prize_idx = -1
                for row in col:
                    if event.control == row.controls[0].content.controls[-1].controls[0]:
                        prize_idx = int(row.controls[0].content.controls[0].controls[0].value)
                        break

                # delete prev col
                db.connect()
                db.delete_data('ships', f'x={x} and y={y} and field_id={field}')
                db.close_connection()

                # add the new col
                db.connect()
                ans = db.insert_data('ships', [x, y, prize_idx, field], columns=['x', 'y', 'prize_id', 'field_id'])
                db.close_connection()
                if ans:
                    page.go('/admin_panel')
                    return

            db.connect()
            prizes = db.select_data('prizes')
            db.close_connection()

            col = []
            for prize in prizes:
                col.append(
                    ft.Row(controls=[
                        ft.Container(
                            content=ft.Column(controls=[
                                ft.Row(controls=[
                                    ft.Text(value=prize[0], color='black', size=12)
                                ]),
                                ft.Row(controls=[
                                    ft.Text(value=prize[1], color='black', size=24)
                                ]),
                                ft.Row(controls=[
                                    ft.Text(value=prize[2], color='black', size=16),
                                ]),
                                ft.Row(controls=[
                                    ft.Image(src=prize[3], width=300, height=400)
                                ]),
                                ft.Row(controls=[
                                    ft.ElevatedButton(
                                        text='Выбрать этот приз',
                                        color='green',
                                        icon_color='white',
                                        icon=ft.icons.SELECT_ALL_ROUNDED,
                                        on_click=choose_prize
                                    )
                                ])
                            ]), bgcolor='white', border_radius=10, border=ft.border.all(8, 'purple'),
                        )
                    ])
                )
            return col

        # get the x and y of the ship
        x, y, field = map(int, str(page.route).split('/')[-1].split('|'))

        page.views.clear()
        page.views.append(
            ft.View(controls=[
                # h1
                ft.Row(controls=[
                    ft.Container(
                        ft.Text(
                            value='Выберите приз, который вы хотите назначить кораблю',
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
                    ft.Column(controls=get_all_prizes(), width=500, height=700, scroll=ft.ScrollMode.ALWAYS)
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], bgcolor=BG)
        )
        page.update()

    else:
        page.go('/')
