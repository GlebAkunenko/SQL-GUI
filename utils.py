import datetime as dt

class Variable:
    def __init__(self, default):
        self.value = default
        self.default = default
        self.handlers = []

    def set(self, value):
        if value == '':
            value = self.default
        self.value = value
        for func in self.handlers:
            func(value)

    def get_callback(self):
        def func(sender, app_data, user_data):
            self.set(app_data)
        return func


def date_callback(var: Variable):
    def func(sender, app_data, user_data):
        date = dt.datetime(app_data['year'] - 100 + 2000, app_data['month'] + 1, app_data['month_day'])
        var.set(date)

    return func
