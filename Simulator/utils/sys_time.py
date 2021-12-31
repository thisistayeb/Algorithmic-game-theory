TODAY = 0


def update_time():
    global TODAY
    # in each update, we increase TODAY by 1 hours
    TODAY += convert_time(hours=1)


def current_date():
    return TODAY


def convert_time(minutes=0, hours=0, days=0, years=0):
    return minutes + hours * 60 + days * 24 * 60 + years * 365 * 24 * 60
