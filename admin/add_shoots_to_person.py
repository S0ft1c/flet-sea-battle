import flet as ft
from db import db
from colors import *
import json


def add_shoots_to_person(page: ft.Page):
    def field_selected(event):
        field_id = -1
        for el in page.views[-1].controls[1].controls:
            if event.control == el.controls[0]:
                field_id = int(el.controls[0].text.split()[-1])
                break

        db.connect()
        f_info = db.select_data('users', f'id = {id}')[0][4]
        if not f_info:
            f_info = {str(field_id): 1}
        else:
            f_info: dict = json.loads(f_info)
            f_info[str(field_id)] = 1 + f_info.get(str(field_id), 0)
        f_info = json.dumps(f_info)
        db.update_data('users', 'shoots', f_info, f'id={id}')
        db.close_connection()
        page.go('/admin_panel')

    if page.session.contains_key('login_admin'):
        id = int(page.route.split('/')[-1])

        # main view
        page.views.clear()
        page.views.append(
            ft.View(controls=[
                ft.Row(),  # empty for the best of us

                ft.Row(scroll=ft.ScrollMode.ALWAYS),
            ])
        )

        # get the fields
        db.connect()
        fields = db.select_data('fields')
        db.close_connection()

        for idx, field in enumerate(fields):
            page.views[-1].controls[1].controls.append(
                ft.Column(controls=[
                    ft.ElevatedButton(
                        text=f'Добавить в поле номер {field[0]}',
                        color='black200',
                        on_click=field_selected
                    )
                ])
            )

        page.update()
    else:
        page.go('/')
