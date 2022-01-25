from agents.agent import Agent
from oracles.oracle import get_token_price
from wallet.wallet import Wallet


class IdealAgent(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        """
        If Basis price is higher than $1, this trader sells all his Basis tokens
        If Basis price is less than $1, this trader will change all his USDs to Basis tokens and then buy bonds
        """
        prices = get_token_price()  # (basis, share, bond)
        if prices[0] == 1:
            pass
        elif prices[0] > 1:
            self.sell_basis(self.wallet.basis // 100)
        elif prices[0] < 1:
            self.buy_basis(self.wallet.usd // 100)
            if prices[0] > prices[2]:
                self.buy_bond(self.wallet.basis // 100)
