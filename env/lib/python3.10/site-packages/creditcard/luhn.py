class Luhn:
    @classmethod
    def checkdigit(cls, card_number):
        """ checks to make sure that the card passes a luhn mod-10 checksum """
        _sum = 0
        num_digits = len(card_number)
        oddeven = num_digits & 1
        for i in range(0, num_digits):
            try:
                digit = int(card_number[i])
            except ValueError:
                return False
            if not ((i & 1) ^ oddeven):
                digit = digit * 2
            if digit > 9:
                digit = digit - 9
            _sum = _sum + digit
        return (_sum % 10) == 0
