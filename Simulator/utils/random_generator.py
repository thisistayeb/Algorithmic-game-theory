import random


def random_hex(length):
    return "".join([hex(random.randint(0, 15))[-1] for i in range(length)])


def generate_wallet_address():
    return random_hex(64)


def generate_bond_address():
    return random_hex(64)


def current_date():
    pass