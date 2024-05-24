from math import sqrt, e


def calculate_level(exp: int) -> int:
    result = abs(sqrt((exp + 1.3) / 0.25)) - 2.3
    return int(result) if result > 0 else 0


def calculate_ratio_upgrading(current_stat: int) -> float:
    # return 20 / (e ** (0.483 * current_stat - 6.6)) # Need Update func
    return -0.19999999999 * current_stat + 20
