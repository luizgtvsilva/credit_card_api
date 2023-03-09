import re


def sanitize(value):
    return "".join(re.findall(r"\w+", value))
