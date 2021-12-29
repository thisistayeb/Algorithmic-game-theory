from agent import Agent
from wallet.wallet import Wallet
import random

class RandomAgent(Agent):
    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def action(self):
        """
        randomly choose to this acrion
        share <-> usd
        basis <-> usd
        basis -> bond
        """
        prices = get_token_price()  # (basis, share, bond)
        if self.wallet.usd > 0:
            amount = random.uniform(0,self.wallet.usd)
            self.buy_basis(amount)
        if self.wallet.basis > 0:
            amount = random.uniform(0,self.wallet.usd)
            self.buy_bond(amount)
            self.sell_basis(amount)
