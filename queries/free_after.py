import dearpygui.dearpygui as dpg

from utils import *
from elements.tables import Table

tag1 = "Q4"
tag2 = "T4"
tag_r = 'r4'
par_r = 'p4'

def free_after(connection):

    with dpg.collapsing_header(label="Освободятся к"):
        # input
        now = dt.datetime.now()
        date = Variable(now)
        records = Variable(0)
        with dpg.group(horizontal=True):
            dpg.add_text("Дата начала")
            dpg.add_date_picker(
                label="Дата начала",
                level=dpg.mvDatePickerLevel_Day,
                default_value={'month_day': now.day, 'year': now.year - 2000 + 100, 'month': now.month - 1},
                callback=date_callback(date)
            )
            with dpg.group(tag=par_r):
                dpg.add_text("Сведения о количестве свободных номеров с указанными характеристиками", wrap=600)
                dpg.add_input_text(label="записей", width=100, enabled=False, default_value=records.value, tag=tag_r, parent=par_r)

        # result
        def get_data() -> list[tuple]:
            with connection() as conn, conn.cursor() as cur:
                args = (
                    date.value,
                )
                sql = "call free_after(%s)"
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