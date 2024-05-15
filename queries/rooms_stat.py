import dearpygui.dearpygui as dpg

from utils import *
from elements.plots import PiePlot

P = '8'

def room_stat(connection):
    # input
    with dpg.collapsing_header(label="Статистика оценок номеров"):
        with connection() as conn, conn.cursor() as cur:
            cur.execute("select address from hotels")
            hotels = [d[0] for d in cur.fetchall()]
            hotel = Variable(hotels[0])
            cur.execute("select r.number from rooms r join hotels h on r.hotel = h.id where h.address = %s", (hotel.value,))
            numbers = [d[0] for d in cur.fetchall()]
            number = Variable(numbers[0])


        def update_numbers(for_hotel):
            with connection() as conn, conn.cursor() as cur:
                cur.execute("select r.number from rooms r join hotels h on r.hotel = h.id where h.address = %s",
                            (for_hotel,))
                numbers = [d[0] for d in cur.fetchall()]

            dpg.delete_item(f"n{P}")
            dpg.add_listbox(numbers, width=100, callback=number.get_callback(), tag=f"n{P}", parent=f"p{P}", label="Номер")

        hotel.handlers.append(update_numbers)


        with dpg.group(horizontal=True):
            with dpg.group(tag=f'r{number}'):
                dpg.add_text("Статистика оценок номеров, составленную по отзывам постояльцев", wrap=600)
                with dpg.group(horizontal=True, tag=f"i{P}"):
                    dpg.add_listbox(hotels, width=500, callback=hotel.get_callback())
                    dpg.add_listbox(numbers, width=100, callback=number.get_callback(), tag=f"n{P}", parent=f"i{P}", label="Номер")

        # result
        def get_data() -> list[tuple]:
            with connection() as conn, conn.cursor() as cur:
                args = (
                    hotel.value,
                    number.value
                )
                sql = """
                select f.score from hotels h 
                join rooms r on r.hotel = h.id
                join contracts c on c.room = r.id
                join feedbacks f on f.contract = c.id
                where h.address = %s and r.number = %s
                """
                cur.execute(sql, args)
                return cur.fetchall()


        def execute(value = 0):
            dpg.delete_item(f'b{P}')
            data = get_data()
            if data:
                data = [d[0] for d in data]
                with dpg.plot(label="Оценки номера", height=400, width=-1, parent=f'p{P}', tag=f'b{P}'):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label="x", lock_min=True)
                    with dpg.plot_axis(dpg.mvYAxis, label="y"):
                        dpg.add_stem_series([i for i in range(1, len(data) + 1)], data)
            else:
                dpg.add_text("Пока нет оценок", parent=f'p{P}', tag=f'b{P}')

        number.handlers.append(execute)
        with dpg.group(tag=f'p{P}'):
            execute()

