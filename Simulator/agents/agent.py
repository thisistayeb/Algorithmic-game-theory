from wallet.wallet import Wallet


class Agent:
    def __init__(self):
        self.wallet = Wallet()

    def add_usd_to_wallet(self, amount):
        self.wallet.add_usd(amount)
