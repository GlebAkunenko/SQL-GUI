import dearpygui.dearpygui as dpg

from utils import *
from elements.tables import Table

P = 6

def persons_info(connection):

    with dpg.collapsing_header(label="Свободные номера"):
        # input

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
            dpg.add_text("Сведения о постояльце из заданного номера: его счет гостинице за дополнительные услуги, поступавшие от него жалобы, виды дополнительных услуг, которыми он пользовался", wrap=600)
            with dpg.group(horizontal=True, tag=f"p{P}"):
                dpg.add_listbox(hotels, width=500, callback=hotel.get_callback())
                dpg.add_listbox(numbers, width=100, callback=number.get_callback(), tag=f"n{P}", parent=f"p{P}", label="Номер")

        with dpg.group(horizontal=True):

            with dpg.group(tag=f"rn{P}"):
                ...


        # def execute(sender, app, user_data):
        #     data = get_data()
        #     table.clear()
        #     table.add_data(data)
        #     records.set(len(data))
        #     dpg.delete_item(tag_r)
        #     dpg.add_input_text(label="записей", width=100, enabled=False, default_value=records.value, tag=tag_r,
        #                        parent=par_r)
        #
        # dpg.add_button(label="Посчитать", callback=execute)
        #
        # with dpg.group(tag=tag1):
        #     table.create()