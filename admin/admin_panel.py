import flet as ft
from colors import *
from db import db

cur_field_selected = -1


def admin_panel(page: ft.Page):
    global cur_field_selected

    def add_btns_fields():
        # receive the data for all the boards
        db.connect()
        fields = db.select_data('fields')
        db.close_connection()
        page.views[-1].controls[1].controls.clear()
        for idx, field in enumerate(fields):
            page.views[-1].controls[1].controls.append(
                ft.Column(controls=[
                    ft.ElevatedButton(
                        text=f'Открыть поле номер {field[0]}',
                        color='black200',
                        on_click=field_selected
                    )
                ])
            )

    def add_ship(event):
        global cur_field_selected
        i = -1
        j = -1
        for ii in range(len(page.views[-1].controls[2].controls[0].controls)):
            try:
                j = (page.views[-1].controls[2].controls[0].controls[ii].controls.index(event.control))
                i = ii
                break
            except:
                pass
        page.go(f'/add_ship/{i}|{j}|{cur_field_selected}')
        return

    def draw_table(cur_field_selected):
        if cur_field_selected != -1:
            db.connect()
            ships_data = db.select_data('ships', f'field_id = {cur_field_selected}')
            db.close_connection()
            db.connect()
            n = int(db.select_data('fields', f'id = {cur_field_selected}')[0][-1])
            db.close_connection()

            page.views[-1].controls[2].controls[0].controls.clear()
            for i in range(n):
                page.views[-1].controls[2].controls[0].controls.append(ft.Row())
                for j in range(n):
                    for ship in ships_data:
                        if i == ship[1] and j == ship[2]:
                            page.views[-1].controls[2].controls[0].controls[i].controls.append(
                                ft.IconButton(icon=ft.icons.LOCAL_SHIPPING, icon_color='blue200',
                                              on_click=add_ship)
                            )
                            break
                    else:
                        page.views[-1].controls[2].controls[0].controls[i].controls.append(
                            ft.IconButton(icon=ft.icons.HOURGLASS_EMPTY, icon_color='blue200',
                                          on_click=add_ship)
                        )
            page.update()

    def add_board(event):
        def create_board(event):
            try:
                n = int(page.views[-1].controls[0].controls[0].value)
                db.connect()
                db.insert_data('fields', [n], columns=['n'])
                page.views.pop()
                add_btns_fields()
                page.update()
            except:
                pass

        page.views.append(
            ft.View(controls=[
                ft.Row(controls=[
                    ft.TextField(label='Введите N поля'),
                    ft.ElevatedButton(
                        text='Создать', bgcolor='blue200', color='white', on_click=create_board
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
            ], horizontal_alignment=ft.alignment.center, vertical_alignment=ft.alignment.center,
                bgcolor=BG,
            )
        )
        page.update()

    def add_prize(event):
        page.go('/add_prize')
        return

    def field_selected(event):
        global cur_field_selected

        text = event.control.text
        cur_field_selected = int(text.split()[-1])
        print(cur_field_selected)
        draw_table(cur_field_selected)

    def logout_admin(event):
        page.session.remove('login_admin')
        page.go('/')
        return

    def go_to_shoots(event):
        page.go('/shoots')
        return

    def get_all_prizes():
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
                            ])
                        ]), bgcolor='white', border_radius=10, border=ft.border.all(8, 'purple'),
                    )
                ])
            )
        return col

    page.views.clear()  # clear all
    if page.session.contains_key('login_admin'):

        page.views.append(  # create a new view
            ft.View(controls=[
                ft.Row(controls=[
                    ft.Column(controls=[
                        ft.ElevatedButton(
                            text='Выйти из аккаунта',
                            icon=ft.icons.EXIT_TO_APP,
                            icon_color='red200',
                            on_click=logout_admin
                        )
                    ]),
                    ft.Column(controls=[
                        ft.ElevatedButton(
                            text='Создать новую доску',
                            color='white', icon=ft.icons.ADD_BOX, icon_color=PINK,
                            on_click=add_board, bgcolor='blue200',
                        )
                    ]),
                    ft.Column(controls=[
                        ft.ElevatedButton(
                            text='Распределить выстрелы',
                            color='white', icon=ft.icons.TROUBLESHOOT, icon_color=PINK,
                            on_click=go_to_shoots, bgcolor='blue200'
                        )
                    ]),
                    ft.Column(controls=[
                        ft.ElevatedButton(
                            text='Создать новый приз',
                            color='white', icon=ft.icons.GRID_GOLDENRATIO, icon_color=PINK,
                            on_click=add_prize, bgcolor='blue200'
                        )
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),

                # all for the fields
                ft.Row(controls=[]),

                # for the while field
                ft.Row(controls=[
                    ft.Column(controls=[]),  # here will be all the table

                    # all the prizes
                    ft.Column(controls=get_all_prizes(), scroll=ft.ScrollMode.ALWAYS, width=500, height=700,
                              spacing=10)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ], bgcolor=BG),
        )
        add_btns_fields()
        page.update()
    else:
        page.go('/')
