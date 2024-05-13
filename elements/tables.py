import dearpygui.dearpygui as dpg

class Table:
    def __init__(self, name: str, parent: str, headers: list[str]):
        self.headers = headers
        self.name = name
        self.parent = parent

    def create(self):
        with dpg.table(header_row=True, row_background=True,
                       borders_innerH=True, borders_outerH=True, borders_innerV=True,
                       borders_outerV=True, delay_search=True, tag=self.name, parent=self.parent, resizable=True):
            for header in self.headers:
                dpg.add_table_column(label=header)

    def add_data(self, data: list[tuple]):
        for row in data:
            with dpg.table_row(parent=self.name):
                for i in range(len(self.headers)):
                    dpg.add_text(str(row[i]))

    def clear(self):
        dpg.delete_item(self.name)
        self.create()
