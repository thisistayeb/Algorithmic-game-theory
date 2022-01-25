import random


def random_hex(length):
    return "".join([hex(random.randint(0, 15))[-1] for _ in range(length)])


def generate_wallet_address():
    return random_hex(64)


def generate_bond_address():
    return random_hex(64)


def random_gauss(mean, std):
    return random.gauss(mean, std)


def random_uniform(begin, end):
    return random.uniform(begin, end)
