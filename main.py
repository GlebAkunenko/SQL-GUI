import dearpygui.dearpygui as dpg
import font
from queries import *

import mysql.connector



def auth(username: str, password: str):
    def connect():
        return mysql.connector.connect(
            host="localhost",
            database="hotel",
            user=username,
            password=password
        )
    return connect


dpg.create_context()
font.set_up()


with dpg.window(tag="Primary Window"):
    connection = auth("moderator", "moderator")
    partner_stat(connection)
    persons_stat(connection)
    free_rooms(connection)
    free_after(connection)
    partners_prefs(connection)
    persons_info(connection)
    room_stat(connection)
    hotels_stat(connection)
    partners_times(connection)


dpg.create_viewport(title='Custom Title', width=600, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()