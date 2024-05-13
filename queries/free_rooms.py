import dearpygui.dearpygui as dpg

from utils import *
from elements.tables import Table

P = 3

def free_rooms(connection):

    with dpg.collapsing_header(label="Свободные номера"):
        # input
        hotel = Variable(0)
        seats = Variable(0)
        flat = Variable(0)
        records = Variable(0)
        with dpg.group(horizontal=True):
            dpg.add_text("Сведения о количестве свободных номеров с указанными характеристиками", wrap=600)

            with dpg.group(tag=f'pr_{P}'):
                dpg.add_input_text(label="отель", width=100, callback=hotel.get_callback())
                dpg.add_input_text(label="мест", width=100, callback=seats.get_callback())
                dpg.add_input_text(label="этаж", width=100, callback=flat.get_callback())
                dpg.add_input_text(label="записей", width=100, enabled=False, default_value='0', tag=f'r_{P}')

        # result
        def get_data() -> list[tuple]:
            with connection() as conn, conn.cursor() as cur:
                args = (
                    hotel.value if hotel.value else 0,
                    seats.value if seats.value else 0,
                    flat.value if flat.value else 0
                )
                sql = "call rooms_stat(%s, %s, %s)"
                print(args)
                cur.execute(sql, args)
                return cur.fetchall()

        table = Table(f't2_{P}', f't1_{P}', [
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
            dpg.delete_item(f'r_{P}')
            dpg.add_input_text(label="записей", width=100, enabled=False, default_value=records.value, tag=f'r_{P}',
                               parent=f'pr_{P}')


        def execute2(val=0): execute(0, 0, 0)
        hotel.handlers.append(execute2)
        seats.handlers.append(execute2)
        flat.handlers.append(execute2)

        with dpg.group(tag=f't1_{P}'):
            table.create()

        execute2()
