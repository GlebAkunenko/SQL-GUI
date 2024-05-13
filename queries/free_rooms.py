import dearpygui.dearpygui as dpg

from utils import *
from elements.tables import Table

P = 3

def free_rooms(connection):

    with dpg.collapsing_header(label="Свободные номера"):
        # input

        with dpg.group():
            dpg.add_text("Сведения о количестве свободных номеров с указанными характеристиками", wrap=600)


        # result
        def get_data() -> list[tuple]:
            with connection() as conn, conn.cursor() as cur:
                args = (
                    hotel.value,
                    seats.value,
                    flat.value
                )
                sql = "call rooms_stat(%s, %s, %s)"
                print(args)
                cur.execute(sql, args)
                return cur.fetchall()

        table = Table(tag2, tag1, [
            "Адрес",
            "Этаж",
            "Номер",
            "Цена"
        ])


        def execute(sender, app, user_data):
            data = get_data()
            table.clear()
            table.add_data(data)
            records.set(len(data))
            dpg.delete_item(tag_r)
            dpg.add_input_text(label="записей", width=100, enabled=False, default_value=records.value, tag=tag_r,
                               parent=par_r)

        dpg.add_button(label="Посчитать", callback=execute)

        with dpg.group(tag=tag1):
            table.create()