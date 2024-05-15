import dearpygui.dearpygui as dpg

from utils import *
from elements.plots import PiePlot

P = '10'

def partners_times(connection):

    with dpg.collapsing_header(label="Сколько дружим?"):
        # input
        with dpg.group():
            dpg.add_text("Информация о времени сотрудничества с разными компаниями")


        def get_data() -> list[tuple]:
            with connection() as conn, conn.cursor() as cur:
                sql = "call partner_duration(0)"
                cur.execute(sql)
                return cur.fetchall()


        def execute(value=0):
            data = get_data()
            [dpg.delete_item(f'b{P}_{i}') for i in range(3)]
            for i, row in enumerate(data):
                with dpg.table_row(parent=f'p{P}', tag=f'b{P}_{i}'):
                    for i in range(3):
                        dpg.add_text(str(row[i]))

        def click(a, b, c): execute()
        dpg.add_button(label="Обновить", callback=click)

        with dpg.table(header_row=True, row_background=True,
                       borders_innerH=True, borders_outerH=True, borders_innerV=True,
                       borders_outerV=True, delay_search=True, tag=f'p{P}', resizable=True):
            for header in ["Компания", "Уже сотрудничаем", "Конец через"]:
                dpg.add_table_column(label=header)


        execute()
