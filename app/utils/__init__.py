from math import sqrt


def calculate_level(exp: int) -> int:
    result = abs(sqrt((exp + 1.3) / 0.25)) - 2.3
    return int(result) if result > 0 else 0
