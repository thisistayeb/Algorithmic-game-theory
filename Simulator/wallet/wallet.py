from utils.random_generator import generate_wallet_address


class Wallet:
    def __init__(self, bac=0, bas=0, usd=0, bonds=None):
        if bonds is None:
            bonds = []
        self.address = generate_wallet_address()
        self.basis = bac
        self.shares = bas
        self.usd = usd
        self.bonds = bonds

    def add_usd(self, amount):
        if self.usd + amount < 0:
            raise "Can't be added to wallet."
        self.usd += amount

    def add_share(self, amount):
        if self.shares + amount < 0:
            raise "Can't be added to wallet."
        self.shares += amount

    def add_basis(self, amount):
        if self.basis + amount < 0:
            raise "Can't be added to wallet."
        self.basis += amount

    def add_bond(self, bond):
        if bond is None:
            raise "Can't be added to wallet."
        self.bonds.append(bond)
