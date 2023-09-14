from datetime import datetime as dt


def prettify_date(date):
    date = dt.strptime(date, "%Y_%m_%d_%H_%M_%S")
    day = date.strftime("%d/%m/%Y")
    time = date.strftime("%I:%M %p")

    return [day, time]

def average(l):
    return sum(l) / len(l) if len(l) > 0 else 0

def sort_by_time(l):
    return dict(sorted(l.items(), key=lambda x: x[1]['show_timing'], reverse=True))
