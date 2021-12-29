from agent import Agent
from wallet.wallet import Wallet
from oracles.oracle import get_token_price


class ShareLover(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        prices = get_token_price()  # (basis, share, bond)
        if self.wallet.usd > 0:
            self.buy_share(self.wallet.usd)
        if prices[0] > 1.2:
            self.sell_basis(self.wallet.basis)

