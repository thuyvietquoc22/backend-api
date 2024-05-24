from math import sqrt, e


def calculate_level(exp: int) -> int:
    result = abs(sqrt((exp + 1.3) / 0.25)) - 2.3
    return int(result) if result > 0 else 0


def calculate_ratio_upgrading(exp: int) -> float:
    level = calculate_level(exp)
    return 20 / (e ** (0.483 * level - 6.6))
