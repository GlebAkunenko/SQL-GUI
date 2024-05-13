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

        with dpg.group(tag=f'result{P}'):

            def show_result(value=0):
                with connection() as conn, conn.cursor() as cur:
                    cur.execute("select id from hotels where address = %s", (hotel.value,))
                    h_id = cur.fetchone()[0]
                    cur.execute("select id from rooms where hotel = %s and number = %s", (h_id, number.value))
                    r_id = cur.fetchone()[0]
                    sql = """
                    select c.person from contracts c
                    join persons p on c.person = p.id
                    where
                        curdate() between c.start and c.end
                        and c.room = %s
                    """
                    cur.execute(sql, (r_id,))
                    p_id = cur.fetchone()

                dpg.delete_item(f'result_body{P}')
                with dpg.group(horizontal=True, parent=f'result{P}', tag=f'result_body{P}'):
                    if p_id is None:
                        dpg.add_text("На данный момент комната не заселена")
                    else:
                        p_id = p_id[0]
                        with connection() as conn, conn.cursor() as cur:
                            cur.execute("select * from persons where id = %s", (p_id,))
                            info = cur.fetchone()
                            cur.execute("select f.content from feedbacks f join contracts c on f.contract = c.id where c.person = %s", (p_id,))
                            feedbacks = cur.fetchall()
                            print(feedbacks)
                        with connection() as conn, conn.cursor() as cur:
                            cur.execute("call bill_info(%s, %s)", (p_id, r_id))
                            bills = cur.fetchall()

                        dpg.add_text(f"""
                        ФИО:\t\t\t\t\t\t{info[2]} {info[1]} {info[3]}
                        Дата рождения:\t\t\t{info[4]}
                        Паспорт:\t\t\t\t{info[6]}
                        """)

                        if bills is not None:
                            with dpg.table(header_row=True, row_background=True,
                                           borders_innerH=True, borders_outerH=True, borders_innerV=True,
                                           borders_outerV=True, delay_search=True, resizable=True, width=500):
                                dpg.add_table_column(label='Услуга')
                                dpg.add_table_column(label='Счёт')

                            for row in bills:
                                with dpg.table_row():
                                    for i in range(2):
                                        dpg.add_text(str(row[i]))

                        if feedbacks:
                            with dpg.table(header_row=True, row_background=True,
                                           borders_innerH=True, borders_outerH=True, borders_innerV=True,
                                           borders_outerV=True, delay_search=True, resizable=True):
                                dpg.add_table_column(label='Жалобы')

                                print(feedbacks)
                                for row in feedbacks:
                                    with dpg.table_row():
                                        if row[0]:
                                            dpg.add_text(str(row[0]))
                        else:
                            dpg.add_text("Жалобы отстутствуют")

            show_result()
            hotel.handlers.append(show_result)
            number.handlers.append(show_result)

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