import random
from string import ascii_uppercase, digits


def generate_random_code():
    return ''.join(random.choices(ascii_uppercase + digits, k=7))
