import re

from .exceptions import BrandNotFound
from .luhn import Luhn
from .utils import sanitize

BRAND_REGEX = {
    "banese": r"^(636117|637473|637470|636659|637472)[0-9]{10,12}$",
    "elo": r"^(401178|401179|431274|438935|451416|457393|457631|457632|504175|627780|636297|636368|(506699|5067[0-6]\d|50677[0-8])|(50900\d|5090[1-9]\d|509[1-9]\d{2})|65003[1-3]|(65003[5-9]|65004\d|65005[0-1])|(65040[5-9]|6504[1-3]\d)|(65048[5-9]|65049\d|6505[0-2]\d|65053[0-8])|(65054[1-9]|6505[5-8]\d|65059[0-8])|(65070\d|65071[0-8])|65072[0-7]|(65090[1-9]|65091\d|650920)|(65165[2-9]|6516[6-7]\d)|(65500\d|65501\d)|(65502[1-9]|6550[3-4]\d|65505[0-8]))[0-9]{10,12}$",  # noqa: E501
    "cabal": r"^(604324|604330|604337|604203|604338)[0-9]{10,12}",
    "softnex": r"^610800",
    "diners": r"^3(?:0[0-5]|[68][0-9])[0-9]{11}$",
    "discover": r"^6(?:011|5[0-9]{2}|4[4-9][0-9]{1}|(22(12[6-9]|1[3-9][0-9]|[2-8][0-9]{2}|9[01][0-9]|92[0-5]$)[0-9]{10}$))[0-9]{12}$",  # noqa: E501
    "hipercard": r"^(38[0-9]{17}|60[0-9]{14})$",
    "amex": r"^3[47][0-9]{13}$",
    "aura": r"^50[0-9]{14,17}$",
    "master": r"^(5[1-5][0-9]{14}|2221[0-9]{12}|222[2-9][0-9]{12}|22[3-9][0-9]{13}|2[3-6][0-9]{14}|27[01][0-9]{13}|2720[0-9]{12})$",  # noqa: E501
    "visa": r"^4[0-9]{12}(?:[0-9]{3})?$",
}


class CreditCard:
    def __init__(self, number):
        self.number = sanitize(number)

    def is_valid(self):
        return all([len(self.number) in range(13, 19), Luhn.checkdigit(self.number)])

    def get_brand(self):
        for brand, regex in BRAND_REGEX.items():
            if re.match(regex, self.number):
                return brand
        raise BrandNotFound("Card number does not match any brand")
