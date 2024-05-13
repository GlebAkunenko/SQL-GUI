import dearpygui.dearpygui as dpg

class PiePlot:
    def __init__(self, tag1: str, tag2: str):
        self.tag1 = tag1
        self.tag2 = tag2

    def create(self):
        with dpg.plot(no_title=True,
                      no_mouse_pos=True,
                      width=250, height=250,
                      tag=self.tag1):
            # create legend
            dpg.add_plot_legend()

            # create x axis
            dpg.add_plot_axis(dpg.mvXAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
            dpg.set_axis_limits(dpg.last_item(), 0, 1)

    def clear(self):
        dpg.delete_item(self.tag2)

    def draw_data(self, values, labels):
        # create y axis
        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True, parent=self.tag1, tag=self.tag2):
            dpg.set_axis_limits(dpg.last_item(), 0, 1)
            dpg.add_pie_series(0.7, 0.35, 0.3, values, labels, normalize=True, format="%.0f")
