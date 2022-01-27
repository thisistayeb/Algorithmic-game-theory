import random


def random_hex(length):
    return "".join([hex(random.randint(0, 15))[-1] for _ in range(length)])


def generate_wallet_address():
    return random_hex(12)


def generate_bond_address():
    return random_hex(12)


def random_gauss(mean, std):
    return random.gauss(mean, std)
