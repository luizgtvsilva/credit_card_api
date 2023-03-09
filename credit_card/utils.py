from datetime import datetime, date
import calendar


def is_valid_date_format(date_str):
    try:
        datetime.strptime(date_str, '%m/%Y')
        return True
    except ValueError:
        return False


def is_date_valid(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = date.today()
        return date_obj > today
    except ValueError:
        return False


def get_last_day_of_month(date_str):
    month, year = date_str.split('/')
    last_day = calendar.monthrange(int(year), int(month))[1]
    return date(int(year), int(month), last_day).strftime('%Y-%m-%d')