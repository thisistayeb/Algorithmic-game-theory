from agents.agent import Agent
from oracles.oracle import get_token_price
from wallet.wallet import Wallet


class HungryTraderAgent(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        """
        This trader sells all of his Basis tokens if the Basis price is double the initial price ($1)
        When the Basis price is less than half of the initial price, the trader will exchange all his USDs for Basis tokens
        """
        prices = get_token_price()  # (basis, share, bond)
        if prices[0] == 0:
            pass
        elif prices[0] > 2:
            self.sell_basis(self.wallet.basis)
        elif prices[0] < 0.5:
            self.buy_basis(self.wallet.usd)
