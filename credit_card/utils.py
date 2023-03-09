from datetime import datetime, date
import calendar
from creditcard import CreditCard
from creditcard.exceptions import BrandNotFound
import hashlib


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


def check_if_cc_is_valid(cc_number):
    cc = CreditCard(cc_number)
    return cc.is_valid()


def get_cc_brand(cc_number):
    cc = CreditCard(cc_number)
    try:
        return cc.get_brand()
    except BrandNotFound:
        return False


def encrypt_cc_number(cc_number):
    cc_number_bytes = cc_number.encode('utf-8')
    hash_object = hashlib.sha256()

    hash_object.update(cc_number_bytes)
    digest_bytes = hash_object.digest()

    digest_hex = digest_bytes.hex()

    return digest_hex
