from wallet.wallet import Wallet
from oracles.exchange import add_transaction


class Agent:
    def __init__(self, wallet: Wallet):
        self.wallet = wallet

    def buy_basis(self, amount):  # this method can be override by its child
        add_transaction("usd", "basis", amount, self.wallet)

    def sell_basis(self, amount):  # this method can be override by its child
        add_transaction("basis", "usd", amount, self.wallet)

    def buy_share(self, amount):  # this method can be override by its child
        add_transaction("usd", "share", amount, self.wallet)

    def sell_share(self, amount):  # this method can be override by its child
        add_transaction("share", "usd", amount, self.wallet)

    def buy_bond(self, amount):  # this method can be override by its child
        add_transaction("basis", "bond", amount, self.wallet)

    def sell_bond(self):  # this method can be override by its child
        pass

    def buy_usd(self, amount):  # this method can be override by its child
        self.wallet.add_usd(amount)

    def sell_usd(self, amount):  # this method can be override by its child
        self.wallet.add_usd(-1 * amount)

    def action(self):  # this method will be overridden by its subclasses
        pass
