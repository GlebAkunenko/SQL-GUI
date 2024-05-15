import dearpygui.dearpygui as dpg

from utils import *
from elements.plots import PiePlot

P = '9'

def hotels_stat(connection):

    with dpg.collapsing_header(label="Доходность отелей"):
        # input
        now = dt.datetime.now().date()
        start_date = Variable(now)
        end_date = Variable(now)
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
                with dpg.group():
                    dpg.add_text("Информацию о доходности всех отелей в выбранном промежутке времени", wrap=600)

        # result
        def get_data() -> list[tuple]:
            with connection() as conn, conn.cursor() as cur:
                args = (
                    start_date.value if not skip_start.value else None,
                    end_date.value if not skip_end.value else None
                )
                sql = "call hotel_profits(%s, %s)"
                cur.execute(sql, args)
                return cur.fetchall()

        with dpg.plot(no_title=True,
                      no_mouse_pos=True,
                      width=500, height=500,
                      tag=f'p{P}'):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
            dpg.set_axis_limits(dpg.last_item(), 0, 1)

        def execute(value=0):
            data = get_data()
            labels = [d[0] for d in data]
            values = [d[1] for d in data]

            dpg.delete_item(f'b{P}')
            with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True, parent=f'p{P}', tag=f'b{P}'):
                dpg.set_axis_limits(dpg.last_item(), 0, 1)
                dpg.add_pie_series(0.5, 0.4, 0.4, values, labels, normalize=True, format="%.0f")

        skip_start.handlers.append(execute)
        skip_end.handlers.append(execute)
        start_date.handlers.append(execute)
        end_date.handlers.append(execute)
        execute()
