import flet as ft
from colors import *
from db import db
import json

cur_field_selected = -1
shoots_on_field = 0
all_shoots = {}


def dashboard(page: ft.Page):
    def logout_user(event):
        page.session.remove('login')
        page.go('/')
        return

    def field_selected(event):
        global cur_field_selected
        for el in page.views[-1].controls[1].controls:
            if event.control == el.controls[0]:
                cur_field_selected = int(el.controls[0].text.split()[-1])
                break
        print(cur_field_selected)
        draw_table(cur_field_selected)
        return

    def add_btns_fields():
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

    def shoot_the_spot(event):

        if all_shoots[str(cur_field_selected)] == 0:
            db.close_connection()
            return

        i, j = -1, -1
        for ii in range(len(page.views[-1].controls[2].controls[0].controls)):
            try:
                j = (page.views[-1].controls[2].controls[0].controls[ii].controls.index(event.control))
                i = ii
                break
            except:
                pass
        print(i, j)

        db.connect()
        prize = db.select_data('ships', f'field_id={cur_field_selected} and x={i} and y={j}')
        db.close_connection()
        if prize:
            prize = prize[0]
            prize_id = int(prize[3])

            db.connect()
            cur_prizes = str(db.select_data('users', f'id={user_id[0]}')[0][-1])
            if not cur_prizes:
                cur_prizes = f'{prize_id}'
            else:
                if prize_id in list(map(int, cur_prizes.split(', '))):
                    page.go('/was_prize')
                    db.close_connection()
                    return

                cur_prizes += f', {prize_id}'

            all_shoots[str(cur_field_selected)] -= 1

            db.update_data('users', 'prizes', cur_prizes, f'id={user_id[0]}')
            db.update_data('users', 'shoots', json.dumps(all_shoots), f'id={user_id[0]}')
            db.close_connection()

            page.go(f'/won_prize/{prize_id}')
            return
        else:
            all_shoots[str(cur_field_selected)] -= 1
            db.connect()
            db.update_data('users', 'shoots', json.dumps(all_shoots), f'id={user_id[0]}')
            db.close_connection()
            page.go('/lost_shoot')
        return

    def draw_table(cur_field_selected):
        global shoots_on_field, all_shoots
        if cur_field_selected != -1:
            db.connect()
            user_shoots = db.select_data('users', f'id={user_id[0]}')[0][4]
            if user_shoots:
                user_shoots = json.loads(user_shoots)
                all_shoots = user_shoots
                if user_shoots.get(str(cur_field_selected), 0):
                    shoots_on_field = user_shoots[str(cur_field_selected)]
                else:
                    shoots_on_field = 0
            else:
                shoots_on_field = 0
            db.close_connection()
            db.connect()
            n = int(db.select_data('fields', f'id = {cur_field_selected}')[0][-1])
            db.close_connection()

            page.views[-1].controls[2].controls.clear()
            page.views[-1].controls[2].controls.append(ft.Column(controls=[], width=500))
            for i in range(n):
                page.views[-1].controls[2].controls[0].controls.append(ft.Row())
                for j in range(n):
                    page.views[-1].controls[2].controls[0].controls[i].controls.append(
                        ft.IconButton(icon=ft.icons.HOURGLASS_EMPTY, icon_color='blue200',
                                      on_click=shoot_the_spot)
                    )
            page.views[-1].controls[2].controls.append(ft.Column(controls=[
                ft.Text(value=f'Ваши выстрелы на данном поле = {shoots_on_field}')
            ]))
            page.update()

    def go_prizes_page(event):
        page.go('/prizes_page')
        return

    if page.session.contains_key('login'):
        user_id = page.session.get('login')

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
                    ]),

                    ft.Column(controls=[
                        ft.ElevatedButton(
                            text='Смотреть мои призы',
                            icon=ft.icons.LOOKS_3_SHARP,
                            icon_color='yellow',
                            on_click=go_prizes_page
                        )
                    ]),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Row(controls=[]),  # for the btns of fields

                ft.Row(controls=[])  # for the ship btns

            ], horizontal_alignment=ft.alignment.center, bgcolor=BG)
        )
        add_btns_fields()
        page.update()

        # TODO: сделать саму логику игры
    else:
        page.go('/')
