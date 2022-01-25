TODAY = 0


def update_time():
    global TODAY
    # in each update, we increase TODAY by 1 hours
    TODAY += convert_time(hours=1)


def current_date():
    return TODAY


def convert_time(hours=0, days=0, years=0):
    return hours + days * 24 + years * 365 * 24


def launcher():
    global TODAY
    TODAY = 0
