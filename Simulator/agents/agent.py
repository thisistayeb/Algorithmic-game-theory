from wallet.wallet import Wallet


class Agent:
    def __init__(self):
        self.wallet = Wallet()

    def add_usd_to_wallet(self, amount):
        self.wallet.add_usd(amount)

    def buy_basis(self):  # this method can be override by its child
        pass

    def sell_basis(self):  # this method can be override by its child
        pass

    def buy_share(self):  # this method can be override by its child
        pass

    def sell_share(self):  # this method can be override by its child
        pass

    def buy_bond(self):  # this method can be override by its child
        pass

    def sell_bond(self):  # this method can be override by its child
        pass

    def buy_usd(self):  # this method can be override by its child
        pass

    def sell_usd(self):  # this method can be override by its child
        pass
