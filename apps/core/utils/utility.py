import re


def normalize_phone_number(value):
    """数字だけに整形"""
    return re.sub(r'\D', '', str(value))


def format_phone_number(value):
    """ハイフン付き整形"""
    value = normalize_phone_number(value)
    if len(value) == 11:
        return f"{value[:3]}-{value[3:7]}-{value[7:]}"
    elif len(value) == 10:
        return f"{value[:2]}-{value[2:6]}-{value[6:]}"
    return value
