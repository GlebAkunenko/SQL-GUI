import dearpygui.dearpygui as dpg

from utils import *
from elements.tables import Table

tag1 = "Q1"
tag2 = "T1"

def partner_stat(connection):

    with dpg.collapsing_header(label="Фирмы и бронь"):
        # input
        now = dt.datetime.now().date()
        start_date = Variable(now)
        end_date = Variable(now)
        limit = Variable(0)
        skip_start = Variable(False)
        skip_end = Variable(False)
        skip_limit = Variable(False)
        with dpg.group(horizontal=True):
            with dpg.group(horizontal=True):
                with dpg.group():
                    dpg.add_text("Дата начала")
                    dpg.add_checkbox(label="Не учитывать", callback=skip_start.get_callback())
                    dpg.add_date_picker(
                        label="Start Date",
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
                with dpg.group():
                    dpg.add_text("Limit")
                    dpg.add_checkbox(label="Не учитывать", callback=skip_limit.get_callback())
                    dpg.add_input_text(decimal=True, callback=limit.get_callback())
                    dpg.add_text("Перечень и общее число фирм, забронировавших места в объеме, не менее указанного, за весь период сотрудничества, либо за некоторый период", wrap=600)

        # result
        def get_data() -> list[tuple]:
            with connection() as conn, conn.cursor() as cur:
                args = (
                    limit.value if not skip_limit.value else 0,
                    start_date.value if not skip_start.value else None,
                    end_date.value if not skip_end.value else None
                )
                sql = "call partners_stat(%s, %s, %s)"
                print(args)
                cur.execute(sql, args)
                return cur.fetchall()

        table = Table(tag2, tag1, [
            "Компания",
            "Количество контрактов"
        ])


        def execute(sender, app, user_data):
            data = get_data()
            table.clear()
            table.add_data(data)

        dpg.add_button(label="Посчитать", callback=execute)

        with dpg.group(tag=tag1):
            table.create()