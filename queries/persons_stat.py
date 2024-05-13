import dearpygui.dearpygui as dpg

from utils import *
from elements.tables import Table

tag1 = "Q2"
tag2 = "T2"
tag_r = 'r2'
par_r = 'p2'

def persons_stat(connection):

    with dpg.collapsing_header(label="Постояльцы заселившиеся в"):
        # input
        now = dt.datetime.now().date()
        start_date = Variable(now)
        end_date = Variable(now)
        hotel = Variable(0)
        flat = Variable(0)
        seats = Variable(0)
        records = Variable(0)
        skip_start = Variable(False)
        skip_end = Variable(False)
        with dpg.group(horizontal=True):
            with dpg.group(horizontal=True):
                with dpg.group():
                    dpg.add_text("Дата начала")
                    dpg.add_checkbox(label="Не учитывать", callback=skip_start.get_callback())
                    dpg.add_date_picker(
                        label="Дата начала",
                        level=dpg.mvDatePickerLevel_Day,
                        default_value={'month_day': now.day, 'year':now.year - 2000 + 100, 'month':now.month - 1},
                        callback=date_callback(start_date)
                        )
                with dpg.group():
                    dpg.add_text("Дата конца")
                    dpg.add_checkbox(label="Не учитывать", callback=skip_end.get_callback())
                    dpg.add_date_picker(
                        label="End Date",
                        level=dpg.mvDatePickerLevel_Day,
                        default_value={'month_day': now.day, 'year':now.year - 2000 + 100, 'month':now.month - 1},
                        callback=date_callback(end_date)
                    )
                with dpg.group(tag=par_r):
                    dpg.add_text("Перечень и общее число постояльцев, заселявшихся в номера с указанными характеристиками за некоторый период", wrap=600)
                    dpg.add_input_text(label="отель", width=100, decimal=True, callback=hotel.get_callback())
                    dpg.add_input_text(label="мест", width=100, decimal=True, callback=seats.get_callback())
                    dpg.add_input_text(label="этаж", width=100, decimal=True, callback=flat.get_callback())
                    dpg.add_input_text(label="записей", width=100, enabled=False, default_value=records.value, tag=tag_r, parent=par_r)

        # result
        def get_data() -> list[tuple]:
            with connection() as conn, conn.cursor() as cur:
                args = (
                    hotel.value,
                    seats.value,
                    flat.value,
                    start_date.value if not skip_start.value else None,
                    end_date.value if not skip_end.value else None
                )
                sql = "call persons_stat(%s, %s, %s, %s, %s)"
                print(args)
                cur.execute(sql, args)
                return cur.fetchall()

        table = Table(tag2, tag1, [
            "№",
            "Имя",
            "Фамилия",
            "Отчество",
            "Отчестсво",
            "Пол",
            "Паспорт",
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