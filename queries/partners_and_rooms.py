import dearpygui.dearpygui as dpg

from utils import *
from elements.plots import PiePlot

number = '5'

def partners_prefs(connection):

    with dpg.collapsing_header(label="Предпочтения партнёров"):
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
                with dpg.group(tag=f'r{number}'):
                    dpg.add_text("Данные об объеме бронирования номеров данной фирмой за указанный период, и каким номерам отдавались предпочтения", wrap=600)
                    with connection() as conn, conn.cursor() as cur:
                        cur.execute("select name from partners order by id;")
                        items = [a[0] for a in cur.fetchall()]
                    partner = Variable(items[0])
                    dpg.add_listbox(items, callback=partner.get_callback(), width=200, label="Партнёр")

        # result
        def get_data() -> list[tuple]:
            with connection() as conn, conn.cursor() as cur:
                args = (
                    start_date.value if not skip_start.value else None,
                    end_date.value if not skip_end.value else None,
                    partner.value
                )
                sql = """
                select r.seats, r.hotel, r.floor from contracts c
                join partners p on c.partner = p.id
                join rooms r on c.room = r.id
                where contract_in_hard_range(c.id, %s, %s) and p.name = %s
                """
                cur.execute(sql, args)
                return cur.fetchall()

        seats_pie = PiePlot(f's{number}_1', f's{number}_2')
        hotel_pie = PiePlot(f'h{number}_1', f'h{number}_2')
        floor_pie = PiePlot(f'f{number}_1', f'f{number}_2')
        with dpg.group(horizontal=True):
            seats_pie.create()
            hotel_pie.create()
            floor_pie.create()

        def execute(sender, app, user_data):
            data = get_data()
            seats = [d[0] for d in data]
            hotel = [d[1] for d in data]
            flats = [d[2] for d in data]
            seats = {
                v: seats.count(v)
                for v in set(seats)
            }
            hotel = {
                v: hotel.count(v)
                for v in set(hotel)
            }
            flats = {
                v: flats.count(v)
                for v in set(flats)
            }
            seats_pie.clear()
            hotel_pie.clear()
            floor_pie.clear()
            seats_pie.draw_data(list(seats.values()), list(seats.keys()))
            hotel_pie.draw_data(list(hotel.values()), list(hotel.keys()))
            floor_pie.draw_data(list(flats.values()), list(flats.keys()))

        def execute2(val): execute(0, 0, 0)
        start_date.handlers.append(execute2)
        end_date.handlers.append(execute2)
        skip_start.handlers.append(execute2)
        skip_end.handlers.append(execute2)
        partner.handlers.append(execute2)
