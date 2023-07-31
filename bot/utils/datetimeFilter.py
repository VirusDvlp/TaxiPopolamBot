import re


def datetime_filter(message) -> bool:
    temp = re.findall(r'''([2]0[2-3]\d-(?:[0][1-9]|[1][0-2])-(?:[1-2][0-9]|[0][1-9]|3[01]) (?:[0-1][0-9]|2[0-3]):[0-5][0-9])''', message.text)
    return bool(temp)
