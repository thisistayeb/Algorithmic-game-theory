from agents.agent import Agent
from oracles.oracle import get_token_price
from wallet.wallet import Wallet


class NaiveTraderAgent(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        """
        If Basis price is higher than $1, this trader sells all his Basis tokens
        If Basis price is less than $1, this trader will change all his USDs to Basis tokens
        """
        prices = get_token_price()  # (basis, share, bond)
        if prices[0] == 1:
            pass
        elif prices[0] > 1:
            self.sell_basis(self.wallet.basis)
        elif (prices[0] < 1) and (prices[2] < prices[0]):
            self.buy_basis(self.wallet.usd)
