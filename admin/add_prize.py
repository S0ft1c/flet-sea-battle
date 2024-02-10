import flet as ft
from colors import *
from db import db

cur_file_selected = None


def add_prize(page: ft.Page):
    global cur_file_selected

    def pick_file_result(event: ft.FilePickerResultEvent):
        global cur_file_selected
        cur_file_selected = event.files
        page.views[-1].controls[2].controls[2].controls[-1].value = cur_file_selected[0].name
        page.update()

    def create_prize(event):
        name = page.views[-1].controls[2].controls[0].controls[0].value
        desc = page.views[-1].controls[2].controls[1].controls[0].value
        if all([name, desc, cur_file_selected]):
            # download file
            upload_url = page.get_upload_url(cur_file_selected[0].name, 60)
            pick_files_dialog.upload([ft.FilePickerUploadFile(
                cur_file_selected[0].name,
                upload_url=upload_url
            )])
            src = f'data/uploads/{cur_file_selected[0].name}'  # create a src for the file

            # write all to db
            db.connect()
            ans = db.insert_data('prizes', [name, desc, src], columns=['name', 'desc', 'src'])
            db.close_connection()
            if ans:
                page.go('/admin_panel')
                return

    page.views.clear()
    if page.session.contains_key('login_admin'):

        # pick file overlay logic
        pick_files_dialog = ft.FilePicker(on_result=pick_file_result)
        page.overlay.append(pick_files_dialog)

        # view
        page.views.append(ft.View(controls=[

            # return to the prev
            ft.Row(controls=[
                ft.Column(controls=[
                    ft.IconButton(icon=ft.icons.EXIT_TO_APP_ROUNDED, icon_color='red200')
                ]),
            ], alignment=ft.MainAxisAlignment.START),

            # h1
            ft.Row(controls=[
                ft.Column(controls=[
                    ft.Container(
                        ft.Text(
                            value='Добавление приза',
                            font_family='Serif',
                            size=52,
                            color='White'
                        ),
                        margin=10, padding=10, border_radius=10, bgcolor=FWG,
                        blur=ft.Blur(10, 0, ft.BlurTileMode.MIRROR),
                        border=ft.border.only(left=ft.border.BorderSide(10, PINK))
                    ),
                ])
            ]),

            # the main logic
            ft.Row(controls=[
                ft.Column(controls=[
                    ft.TextField(
                        label='Название приза',
                        border_radius=15, border_width=2, border_color=PINK,
                        text_size=24, color='white', bgcolor=FWG
                    )
                ]),
                ft.Column(controls=[
                    ft.TextField(
                        label='Описание приза',
                        border_radius=15, border_width=2, border_color=PINK,
                        text_size=24, color='white', bgcolor=FWG,
                    )
                ]),

                # pick picture button
                ft.Column(controls=[
                    ft.ElevatedButton(
                        text='Загрузить изображение',
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=False)
                    ),
                    ft.Text(
                        value=cur_file_selected,
                        color='white',
                        bgcolor=FWG,
                    )
                ]),

                ft.Column(controls=[
                    ft.ElevatedButton(
                        text='Создать приз',
                        icon=ft.icons.ADD_CARD,
                        on_click=create_prize
                    )
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        ], bgcolor=BG, horizontal_alignment=ft.alignment.bottom_center))
        page.update()
    else:
        page.go('/')
