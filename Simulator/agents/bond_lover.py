from agents.agent import Agent
from wallet.wallet import Wallet
from oracles.oracle import get_token_price


class BondLover(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        prices = get_token_price()  # (basis, share, bond)
        if prices[0] > 1.2:
            self.sell_basis(self.wallet.usd // 2)
        else:
            if self.wallet.usd > 0:
                self.buy_basis(self.wallet.usd)
            if self.wallet.basis > 0:
                self.buy_bond(self.wallet.basis)
