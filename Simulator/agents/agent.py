from wallet.wallet import Wallet


class Agent:
    def __init__(self, wallet: Wallet):
        self.wallet = wallet

    def buy_basis(self, amount):  # this method can be override by its child
        self.wallet.add_basis(amount)

    def sell_basis(self, amount):  # this method can be override by its child
        self.wallet.add_basis(-1 * amount)

    def buy_share(self, amount):  # this method can be override by its child
        self.wallet.add_share(amount)

    def sell_share(self, amount):  # this method can be override by its child
        self.wallet.add_share(-1 * amount)

    def buy_bond(self, bond):  # this method can be override by its child
        self.wallet.add_bond(bond)

    def sell_bond(self):  # this method can be override by its child
        pass

    def buy_usd(self, amount):  # this method can be override by its child
        self.wallet.add_usd(amount)

    def sell_usd(self, amount):  # this method can be override by its child
        self.wallet.add_usd(-1 * amount)

    def action(self):  # this method will be overridden by its subclasses
        pass
