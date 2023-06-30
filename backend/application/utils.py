import datetime as dt
def prettify_date(date):
    date = dt.strptime(date, "%Y_%m_%d_%H_%M_%S")
    day = date.strftime("%d/%m/%Y")
    time = date.strftime("%I:%M %p")

    return [day, time]